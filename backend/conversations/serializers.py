"""
DRF Serializers for Conversations and Messages.
"""
from rest_framework import serializers
from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model."""
    
    class Meta:
        model = Message
        fields = [
            'id',
            'conversation',
            'content',
            'sender',
            'timestamp',
            'tokens_used',
            'model_used',
            'created_at'
        ]
        read_only_fields = ['id', 'timestamp', 'created_at']


class ConversationListSerializer(serializers.ModelSerializer):
    """Serializer for listing conversations (basic info only)."""
    message_count = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = [
            'id',
            'title',
            'status',
            'start_timestamp',
            'end_timestamp',
            'message_count',
            'duration',
            'last_message',
            'topics',
            'sentiment',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_message_count(self, obj):
        """Get the total number of messages in the conversation."""
        return obj.get_message_count()
    
    def get_duration(self, obj):
        """Get the conversation duration in seconds."""
        return obj.get_duration()
    
    def get_last_message(self, obj):
        """Get the last message content preview."""
        last_message = obj.messages.last()
        if last_message:
            content = last_message.content[:100]
            return {
                'content': content,
                'sender': last_message.sender,
                'timestamp': last_message.timestamp
            }
        return None


class ConversationDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed conversation view with all messages."""
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = [
            'id',
            'title',
            'status',
            'start_timestamp',
            'end_timestamp',
            'summary',
            'topics',
            'key_points',
            'sentiment',
            'message_count',
            'duration',
            'messages',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_message_count(self, obj):
        """Get the total number of messages in the conversation."""
        return obj.get_message_count()
    
    def get_duration(self, obj):
        """Get the conversation duration in seconds."""
        return obj.get_duration()


class ConversationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new conversation."""
    
    class Meta:
        model = Conversation
        fields = ['id', 'title', 'status']
        read_only_fields = ['id', 'status']


class ChatMessageSerializer(serializers.Serializer):
    """Serializer for sending chat messages."""
    conversation_id = serializers.IntegerField()
    message = serializers.CharField()


class EndConversationSerializer(serializers.Serializer):
    """Serializer for ending a conversation."""
    conversation_id = serializers.IntegerField()


class QueryConversationsSerializer(serializers.Serializer):
    """Serializer for querying past conversations."""
    query = serializers.CharField()
    date_from = serializers.DateTimeField(required=False, allow_null=True)
    date_to = serializers.DateTimeField(required=False, allow_null=True)
    limit = serializers.IntegerField(default=5, min_value=1, max_value=20)

