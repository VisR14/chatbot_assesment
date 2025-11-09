"""
Database models for the Chat Portal application.
"""
from django.db import models
from django.utils import timezone


class Conversation(models.Model):
    """
    Model representing a conversation thread.
    Stores metadata including title, timestamps, status, and AI-generated summary.
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('ended', 'Ended'),
    ]
    
    title = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    start_timestamp = models.DateTimeField(default=timezone.now)
    end_timestamp = models.DateTimeField(null=True, blank=True)
    summary = models.TextField(blank=True, null=True)
    
    # Metadata fields for conversation intelligence
    topics = models.JSONField(default=list, blank=True)  # List of extracted topics
    key_points = models.JSONField(default=list, blank=True)  # List of key points/decisions
    sentiment = models.CharField(max_length=50, blank=True, null=True)  # Overall sentiment
    
    # Embedding for semantic search (stored as JSON array)
    embedding = models.JSONField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_timestamp']
        indexes = [
            models.Index(fields=['-start_timestamp']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Conversation {self.id}: {self.title or 'Untitled'}"
    
    def get_duration(self):
        """Calculate conversation duration in seconds."""
        if self.end_timestamp:
            return (self.end_timestamp - self.start_timestamp).total_seconds()
        return None
    
    def get_message_count(self):
        """Get the total number of messages in this conversation."""
        return self.messages.count()


class Message(models.Model):
    """
    Model representing individual messages within a conversation.
    Stores message content, sender, timestamp, and related conversation.
    """
    SENDER_CHOICES = [
        ('user', 'User'),
        ('ai', 'AI'),
    ]
    
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    content = models.TextField()
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    timestamp = models.DateTimeField(default=timezone.now)
    
    # Optional metadata
    tokens_used = models.IntegerField(null=True, blank=True)  # Track token usage for AI responses
    model_used = models.CharField(max_length=100, blank=True, null=True)  # Track which AI model was used
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['conversation', 'timestamp']),
            models.Index(fields=['sender']),
        ]
    
    def __str__(self):
        return f"{self.sender}: {self.content[:50]}..."

