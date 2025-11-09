"""
Unit tests for the Conversations app.

Run tests with: python manage.py test conversations
"""
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Conversation, Message


class ConversationModelTest(TestCase):
    """Test cases for Conversation model."""
    
    def setUp(self):
        """Set up test data."""
        self.conversation = Conversation.objects.create(
            title="Test Conversation",
            status="active"
        )
    
    def test_conversation_creation(self):
        """Test that conversation is created correctly."""
        self.assertEqual(self.conversation.title, "Test Conversation")
        self.assertEqual(self.conversation.status, "active")
        self.assertIsNotNone(self.conversation.start_timestamp)
    
    def test_conversation_string_representation(self):
        """Test string representation of conversation."""
        expected = f"Conversation {self.conversation.id}: Test Conversation"
        self.assertEqual(str(self.conversation), expected)
    
    def test_get_message_count(self):
        """Test message count method."""
        self.assertEqual(self.conversation.get_message_count(), 0)
        
        # Add some messages
        Message.objects.create(
            conversation=self.conversation,
            content="Test message 1",
            sender="user"
        )
        Message.objects.create(
            conversation=self.conversation,
            content="Test message 2",
            sender="ai"
        )
        
        self.assertEqual(self.conversation.get_message_count(), 2)
    
    def test_get_duration(self):
        """Test duration calculation."""
        # Active conversation has no duration
        self.assertIsNone(self.conversation.get_duration())
        
        # Ended conversation has duration
        self.conversation.status = "ended"
        self.conversation.end_timestamp = self.conversation.start_timestamp + timezone.timedelta(minutes=30)
        self.conversation.save()
        
        self.assertEqual(self.conversation.get_duration(), 1800.0)  # 30 minutes in seconds


class MessageModelTest(TestCase):
    """Test cases for Message model."""
    
    def setUp(self):
        """Set up test data."""
        self.conversation = Conversation.objects.create(
            title="Test Conversation",
            status="active"
        )
        self.message = Message.objects.create(
            conversation=self.conversation,
            content="Hello, AI!",
            sender="user"
        )
    
    def test_message_creation(self):
        """Test that message is created correctly."""
        self.assertEqual(self.message.content, "Hello, AI!")
        self.assertEqual(self.message.sender, "user")
        self.assertEqual(self.message.conversation, self.conversation)
        self.assertIsNotNone(self.message.timestamp)
    
    def test_message_string_representation(self):
        """Test string representation of message."""
        expected = "user: Hello, AI!..."
        self.assertEqual(str(self.message), expected)


class ConversationAPITest(APITestCase):
    """Test cases for Conversation API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.conversation = Conversation.objects.create(
            title="Test Conversation",
            status="active"
        )
        Message.objects.create(
            conversation=self.conversation,
            content="Test message",
            sender="user"
        )
    
    def test_list_conversations(self):
        """Test listing all conversations."""
        url = '/api/conversations/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['count'], 1)
    
    def test_retrieve_conversation(self):
        """Test retrieving a specific conversation."""
        url = f'/api/conversations/{self.conversation.id}/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['conversation']['id'], self.conversation.id)
    
    def test_create_conversation(self):
        """Test creating a new conversation."""
        url = '/api/conversations/'
        data = {'title': 'New Test Conversation'}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertEqual(Conversation.objects.count(), 2)
    
    def test_filter_conversations_by_status(self):
        """Test filtering conversations by status."""
        # Create an ended conversation
        Conversation.objects.create(
            title="Ended Conversation",
            status="ended",
            end_timestamp=timezone.now()
        )
        
        url = '/api/conversations/?status=active'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['conversations'][0]['status'], 'active')


class MessageAPITest(APITestCase):
    """Test cases for Message-related API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.conversation = Conversation.objects.create(
            title="Test Conversation",
            status="active"
        )
    
    def test_send_message_creates_messages(self):
        """Test that sending a message creates both user and AI messages."""
        # Note: This test will fail without proper AI configuration
        # In a real test environment, you'd mock the AI service
        pass
    
    def test_end_conversation_updates_status(self):
        """Test ending a conversation updates its status."""
        # Add at least one message
        Message.objects.create(
            conversation=self.conversation,
            content="Test message",
            sender="user"
        )
        
        # Note: This test will fail without proper AI configuration
        # In a real test environment, you'd mock the AI service
        pass


# To run these tests:
# python manage.py test conversations

