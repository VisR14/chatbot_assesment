"""
AI Integration Module for Chat Portal.

This module handles all AI-powered features including:
- Real-time chat with LLM
- Conversation summarization
- Intelligent query answering about past conversations
- Semantic search and embeddings
- Topic extraction and sentiment analysis
"""
import os
import json
from typing import List, Dict, Any, Optional
from django.conf import settings


class AIService:
    """
    Main AI service class that handles all AI operations.
    Supports multiple AI providers: OpenAI, Anthropic, Google Gemini, and LM Studio.
    """
    
    def __init__(self):
        self.provider = settings.AI_PROVIDER
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the AI client based on the configured provider."""
        if self.provider == 'openai':
            try:
                import openai
                openai.api_key = settings.OPENAI_API_KEY
                self.client = openai
                self.model = "gpt-3.5-turbo"
            except ImportError:
                raise ImportError("OpenAI library not installed. Run: pip install openai")
        
        elif self.provider == 'anthropic':
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
                self.model = "claude-3-sonnet-20240229"
            except ImportError:
                raise ImportError("Anthropic library not installed. Run: pip install anthropic")
        
        elif self.provider == 'gemini':
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self.client = genai
                self.model = "gemini-pro"
            except ImportError:
                raise ImportError("Google Generative AI library not installed. Run: pip install google-generativeai")
        
        elif self.provider == 'lmstudio':
            try:
                import openai
                # LM Studio uses OpenAI-compatible API
                openai.api_key = "lm-studio"  # Dummy key for local server
                openai.api_base = settings.LM_STUDIO_BASE_URL
                self.client = openai
                self.model = "local-model"
            except ImportError:
                raise ImportError("OpenAI library not installed. Run: pip install openai")
    
    def chat(self, messages: List[Dict[str, str]], stream: bool = False) -> Dict[str, Any]:
        """
        Send messages to AI and get response.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            stream: Whether to stream the response
        
        Returns:
            Dict containing AI response and metadata
        """
        try:
            if self.provider == 'openai' or self.provider == 'lmstudio':
                return self._chat_openai(messages, stream)
            elif self.provider == 'anthropic':
                return self._chat_anthropic(messages)
            elif self.provider == 'gemini':
                return self._chat_gemini(messages)
        except Exception as e:
            return {
                'response': f"Error communicating with AI: {str(e)}",
                'error': True,
                'model': self.model
            }
    
    def _chat_openai(self, messages: List[Dict[str, str]], stream: bool = False) -> Dict[str, Any]:
        """Handle OpenAI/LM Studio chat requests."""
        response = self.client.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=1000,
            stream=stream
        )
        
        if stream:
            return {'stream': response, 'model': self.model}
        else:
            return {
                'response': response.choices[0].message.content,
                'tokens_used': response.usage.total_tokens,
                'model': self.model,
                'error': False
            }
    
    def _chat_anthropic(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """Handle Anthropic Claude chat requests."""
        # Convert messages format for Claude
        system_message = ""
        claude_messages = []
        
        for msg in messages:
            if msg['role'] == 'system':
                system_message = msg['content']
            else:
                claude_messages.append({
                    'role': msg['role'],
                    'content': msg['content']
                })
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            system=system_message,
            messages=claude_messages
        )
        
        return {
            'response': response.content[0].text,
            'tokens_used': response.usage.input_tokens + response.usage.output_tokens,
            'model': self.model,
            'error': False
        }
    
    def _chat_gemini(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """Handle Google Gemini chat requests."""
        model = self.client.GenerativeModel(self.model)
        
        # Convert messages to Gemini format
        prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
        
        response = model.generate_content(prompt)
        
        return {
            'response': response.text,
            'tokens_used': None,  # Gemini doesn't provide token count in the same way
            'model': self.model,
            'error': False
        }
    
    def generate_summary(self, messages: List[Dict[str, str]]) -> str:
        """
        Generate a summary of a conversation.
        
        Args:
            messages: List of conversation messages
        
        Returns:
            Summary text
        """
        conversation_text = "\n".join([
            f"{msg.get('sender', msg.get('role'))}: {msg['content']}"
            for msg in messages
        ])
        
        summary_prompt = [
            {
                'role': 'system',
                'content': 'You are an AI assistant that creates concise, informative summaries of conversations.'
            },
            {
                'role': 'user',
                'content': f"Please provide a concise summary of the following conversation:\n\n{conversation_text}"
            }
        ]
        
        result = self.chat(summary_prompt)
        return result.get('response', 'Summary generation failed')
    
    def extract_topics(self, messages: List[Dict[str, str]]) -> List[str]:
        """
        Extract main topics from a conversation.
        
        Args:
            messages: List of conversation messages
        
        Returns:
            List of topic strings
        """
        conversation_text = "\n".join([
            f"{msg.get('sender', msg.get('role'))}: {msg['content']}"
            for msg in messages
        ])
        
        topic_prompt = [
            {
                'role': 'system',
                'content': 'You are an AI that extracts key topics from conversations. Return only a JSON array of topics.'
            },
            {
                'role': 'user',
                'content': f"Extract 3-5 main topics from this conversation as a JSON array:\n\n{conversation_text}"
            }
        ]
        
        result = self.chat(topic_prompt)
        response_text = result.get('response', '[]')
        
        try:
            # Try to parse JSON response
            topics = json.loads(response_text)
            if isinstance(topics, list):
                return topics[:5]  # Limit to 5 topics
        except json.JSONDecodeError:
            # Fallback: split by commas if not valid JSON
            topics = [t.strip() for t in response_text.split(',')]
            return topics[:5]
        
        return []
    
    def analyze_sentiment(self, messages: List[Dict[str, str]]) -> str:
        """
        Analyze the overall sentiment of a conversation.
        
        Args:
            messages: List of conversation messages
        
        Returns:
            Sentiment string (e.g., 'positive', 'negative', 'neutral')
        """
        conversation_text = "\n".join([
            f"{msg.get('sender', msg.get('role'))}: {msg['content']}"
            for msg in messages
        ])
        
        sentiment_prompt = [
            {
                'role': 'system',
                'content': 'You are an AI that analyzes sentiment. Respond with only one word: positive, negative, or neutral.'
            },
            {
                'role': 'user',
                'content': f"What is the overall sentiment of this conversation?\n\n{conversation_text}"
            }
        ]
        
        result = self.chat(sentiment_prompt)
        sentiment = result.get('response', 'neutral').lower().strip()
        
        # Ensure valid sentiment
        if sentiment not in ['positive', 'negative', 'neutral']:
            sentiment = 'neutral'
        
        return sentiment
    
    def extract_key_points(self, messages: List[Dict[str, str]]) -> List[str]:
        """
        Extract key points, decisions, and action items from a conversation.
        
        Args:
            messages: List of conversation messages
        
        Returns:
            List of key point strings
        """
        conversation_text = "\n".join([
            f"{msg.get('sender', msg.get('role'))}: {msg['content']}"
            for msg in messages
        ])
        
        keypoints_prompt = [
            {
                'role': 'system',
                'content': 'You are an AI that extracts key points, decisions, and action items. Return a JSON array of strings.'
            },
            {
                'role': 'user',
                'content': f"Extract key points, decisions, and action items from this conversation as a JSON array:\n\n{conversation_text}"
            }
        ]
        
        result = self.chat(keypoints_prompt)
        response_text = result.get('response', '[]')
        
        try:
            key_points = json.loads(response_text)
            if isinstance(key_points, list):
                return key_points[:10]  # Limit to 10 key points
        except json.JSONDecodeError:
            # Fallback: split by newlines or bullets
            lines = response_text.split('\n')
            key_points = [line.strip('- •*').strip() for line in lines if line.strip()]
            return key_points[:10]
        
        return []
    
    def query_conversations(self, query: str, conversations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Query past conversations using natural language.
        
        Args:
            query: User's question about past conversations
            conversations: List of conversation data to search through
        
        Returns:
            Dict containing AI response and relevant conversation excerpts
        """
        # Build context from conversations
        context_parts = []
        for conv in conversations:
            conv_text = f"\n--- Conversation {conv['id']} ({conv['start_timestamp']}) ---\n"
            conv_text += f"Title: {conv.get('title', 'Untitled')}\n"
            conv_text += f"Summary: {conv.get('summary', 'No summary')}\n"
            conv_text += f"Topics: {', '.join(conv.get('topics', []))}\n"
            
            # Include some message samples
            messages = conv.get('messages', [])[:5]  # First 5 messages
            for msg in messages:
                conv_text += f"{msg['sender']}: {msg['content'][:200]}...\n"
            
            context_parts.append(conv_text)
        
        context = "\n".join(context_parts)
        
        query_prompt = [
            {
                'role': 'system',
                'content': 'You are an AI assistant that helps users find information in their past conversations. Provide clear, specific answers with references to conversation IDs when relevant.'
            },
            {
                'role': 'user',
                'content': f"Based on these past conversations:\n\n{context}\n\nUser question: {query}\n\nProvide a helpful answer with specific references."
            }
        ]
        
        result = self.chat(query_prompt)
        
        return {
            'answer': result.get('response', 'Unable to answer query'),
            'relevant_conversations': [conv['id'] for conv in conversations],
            'error': result.get('error', False)
        }
    
    def semantic_search(self, query: str, conversations: List[Dict[str, Any]], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Perform semantic search across conversations.
        
        Args:
            query: Search query
            conversations: List of all conversations
            limit: Maximum number of results
        
        Returns:
            List of relevant conversations ranked by relevance
        """
        # Simple keyword-based search for now
        # In a production system, you would use embeddings and vector similarity
        
        query_lower = query.lower()
        scored_conversations = []
        
        for conv in conversations:
            score = 0
            
            # Check title
            if conv.get('title') and query_lower in conv['title'].lower():
                score += 5
            
            # Check summary
            if conv.get('summary') and query_lower in conv['summary'].lower():
                score += 3
            
            # Check topics
            topics = conv.get('topics', [])
            for topic in topics:
                if query_lower in topic.lower():
                    score += 2
            
            # Check messages
            messages = conv.get('messages', [])
            for msg in messages:
                if query_lower in msg['content'].lower():
                    score += 1
            
            if score > 0:
                scored_conversations.append((score, conv))
        
        # Sort by score and return top results
        scored_conversations.sort(key=lambda x: x[0], reverse=True)
        return [conv for score, conv in scored_conversations[:limit]]


# Singleton instance
_ai_service = None


def get_ai_service() -> AIService:
    """Get or create the AI service singleton instance."""
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService()
    return _ai_service

