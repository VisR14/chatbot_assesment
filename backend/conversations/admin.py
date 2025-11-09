"""
Django admin configuration for Conversations and Messages.
"""
from django.contrib import admin
from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """Admin interface for Conversation model."""
    list_display = ['id', 'title', 'status', 'start_timestamp', 'end_timestamp', 'get_message_count']
    list_filter = ['status', 'start_timestamp']
    search_fields = ['title', 'summary']
    readonly_fields = ['created_at', 'updated_at', 'get_duration']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'status', 'start_timestamp', 'end_timestamp')
        }),
        ('AI Analysis', {
            'fields': ('summary', 'topics', 'key_points', 'sentiment')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'get_duration'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Admin interface for Message model."""
    list_display = ['id', 'conversation', 'sender', 'timestamp', 'content_preview']
    list_filter = ['sender', 'timestamp']
    search_fields = ['content']
    readonly_fields = ['created_at']
    
    def content_preview(self, obj):
        """Display truncated content in admin list."""
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content Preview'

