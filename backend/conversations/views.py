"""
API Views for Chat Portal.

Implements all REST API endpoints for conversation management and AI features.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q

from .models import Conversation, Message
from .serializers import (
    ConversationListSerializer,
    ConversationDetailSerializer,
    ConversationCreateSerializer,
    MessageSerializer,
    ChatMessageSerializer,
    EndConversationSerializer,
    QueryConversationsSerializer
)
from .ai_service import get_ai_service


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing conversations.
    
    Provides CRUD operations and custom actions for conversation management.
    """
    queryset = Conversation.objects.all()
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return ConversationListSerializer
        elif self.action == 'retrieve':
            return ConversationDetailSerializer
        elif self.action == 'create':
            return ConversationCreateSerializer
        return ConversationDetailSerializer
    
    def list(self, request):
        """
        GET /api/conversations/
        Retrieve all conversations with basic info.
        """
        conversations = self.get_queryset()
        
        # Optional filters
        status_filter = request.query_params.get('status')
        if status_filter:
            conversations = conversations.filter(status=status_filter)
        
        search = request.query_params.get('search')
        if search:
            conversations = conversations.filter(
                Q(title__icontains=search) | 
                Q(summary__icontains=search)
            )
        
        serializer = self.get_serializer(conversations, many=True)
        return Response({
            'success': True,
            'count': conversations.count(),
            'conversations': serializer.data
        })
    
    def retrieve(self, request, pk=None):
        """
        GET /api/conversations/{id}/
        Get a specific conversation with full message history.
        """
        try:
            conversation = self.get_object()
            serializer = self.get_serializer(conversation)
            return Response({
                'success': True,
                'conversation': serializer.data
            })
        except Conversation.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Conversation not found'
            }, status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request):
        """
        POST /api/conversations/
        Create a new conversation.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            conversation = serializer.save(status='active')
            return Response({
                'success': True,
                'conversation': ConversationDetailSerializer(conversation).data,
                'message': 'Conversation created successfully'
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def send_message(self, request):
        """
        POST /api/conversations/send_message/
        Send a message in a conversation and get AI response.
        
        Request body:
        {
            "conversation_id": 1,
            "message": "User message content"
        }
        """
        serializer = ChatMessageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        conversation_id = serializer.validated_data['conversation_id']
        user_message = serializer.validated_data['message']
        
        try:
            conversation = Conversation.objects.get(id=conversation_id)
            
            if conversation.status != 'active':
                return Response({
                    'success': False,
                    'error': 'Conversation is not active'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Save user message
            user_msg = Message.objects.create(
                conversation=conversation,
                content=user_message,
                sender='user'
            )
            
            # Get conversation history for context
            messages = conversation.messages.all()
            ai_messages = [
                {'role': 'system', 'content': 'You are a helpful AI assistant.'}
            ]
            
            for msg in messages:
                role = 'user' if msg.sender == 'user' else 'assistant'
                ai_messages.append({'role': role, 'content': msg.content})
            
            # Get AI response
            ai_service = get_ai_service()
            ai_result = ai_service.chat(ai_messages)
            
            if ai_result.get('error'):
                return Response({
                    'success': False,
                    'error': ai_result.get('response', 'AI service error')
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # Save AI response
            ai_msg = Message.objects.create(
                conversation=conversation,
                content=ai_result['response'],
                sender='ai',
                tokens_used=ai_result.get('tokens_used'),
                model_used=ai_result.get('model')
            )
            
            # Update conversation title if it's the first exchange
            if conversation.message_count == 2 and not conversation.title:
                # Generate title from first message
                title = user_message[:50] + ('...' if len(user_message) > 50 else '')
                conversation.title = title
                conversation.save()
            
            return Response({
                'success': True,
                'user_message': MessageSerializer(user_msg).data,
                'ai_response': MessageSerializer(ai_msg).data
            })
        
        except Conversation.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Conversation not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Error processing message: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def end_conversation(self, request):
        """
        POST /api/conversations/end_conversation/
        End a conversation and generate AI summary.
        
        Request body:
        {
            "conversation_id": 1
        }
        """
        serializer = EndConversationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        conversation_id = serializer.validated_data['conversation_id']
        
        try:
            conversation = Conversation.objects.get(id=conversation_id)
            
            if conversation.status == 'ended':
                return Response({
                    'success': False,
                    'error': 'Conversation is already ended'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Get all messages for analysis
            messages = list(conversation.messages.values('sender', 'content'))
            
            if not messages:
                return Response({
                    'success': False,
                    'error': 'Cannot end conversation with no messages'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Generate AI analysis
            ai_service = get_ai_service()
            
            # Generate summary
            summary = ai_service.generate_summary(messages)
            
            # Extract topics
            topics = ai_service.extract_topics(messages)
            
            # Analyze sentiment
            sentiment = ai_service.analyze_sentiment(messages)
            
            # Extract key points
            key_points = ai_service.extract_key_points(messages)
            
            # Update conversation
            conversation.status = 'ended'
            conversation.end_timestamp = timezone.now()
            conversation.summary = summary
            conversation.topics = topics
            conversation.sentiment = sentiment
            conversation.key_points = key_points
            conversation.save()
            
            return Response({
                'success': True,
                'conversation': ConversationDetailSerializer(conversation).data,
                'message': 'Conversation ended and analyzed successfully'
            })
        
        except Conversation.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Conversation not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Error ending conversation: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def query_conversations(self, request):
        """
        POST /api/conversations/query_conversations/
        Query AI about past conversations using natural language.
        
        Request body:
        {
            "query": "What did I discuss about travel?",
            "date_from": "2024-01-01T00:00:00Z" (optional),
            "date_to": "2024-12-31T23:59:59Z" (optional),
            "limit": 5 (optional)
        }
        """
        serializer = QueryConversationsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        query = serializer.validated_data['query']
        date_from = serializer.validated_data.get('date_from')
        date_to = serializer.validated_data.get('date_to')
        limit = serializer.validated_data.get('limit', 5)
        
        try:
            # Filter ended conversations
            conversations = Conversation.objects.filter(status='ended')
            
            # Apply date filters
            if date_from:
                conversations = conversations.filter(start_timestamp__gte=date_from)
            if date_to:
                conversations = conversations.filter(start_timestamp__lte=date_to)
            
            # Get AI service
            ai_service = get_ai_service()
            
            # Perform semantic search
            all_conversations = []
            for conv in conversations:
                conv_data = ConversationDetailSerializer(conv).data
                all_conversations.append(conv_data)
            
            relevant_conversations = ai_service.semantic_search(query, all_conversations, limit)
            
            # Query AI for answer
            if relevant_conversations:
                result = ai_service.query_conversations(query, relevant_conversations)
                
                return Response({
                    'success': True,
                    'query': query,
                    'answer': result['answer'],
                    'relevant_conversations': relevant_conversations,
                    'count': len(relevant_conversations)
                })
            else:
                return Response({
                    'success': True,
                    'query': query,
                    'answer': 'No relevant conversations found for your query.',
                    'relevant_conversations': [],
                    'count': 0
                })
        
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Error querying conversations: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

