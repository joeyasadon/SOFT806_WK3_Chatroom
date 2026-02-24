from django.contrib import admin
from .models import (
    UserProfile, PublicChatHistory, PrivateMessage, 
    GroupChatroom, GroupChatroomMember, GroupMessage,
    ChatFile, ChatImage
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'display_name', 'status', 'last_seen', 'is_active']
    list_filter = ['status', 'is_active', 'created_at']
    search_fields = ['username', 'display_name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(PublicChatHistory)
class PublicChatHistoryAdmin(admin.ModelAdmin):
    list_display = ['author', 'content_preview', 'timestamp', 'message_type', 'edited']
    list_filter = ['message_type', 'edited', 'timestamp']
    search_fields = ['author__username', 'author__display_name', 'content']
    readonly_fields = ['timestamp', 'edited_at']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'


@admin.register(PrivateMessage)
class PrivateMessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'content_preview', 'timestamp', 'is_read']
    list_filter = ['is_read', 'message_type', 'timestamp']
    search_fields = ['sender__username', 'sender__display_name', 'receiver__username', 'receiver__display_name', 'content']
    readonly_fields = ['timestamp', 'edited_at', 'read_at']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'


@admin.register(GroupChatroom)
class GroupChatroomAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'created_at', 'is_active', 'is_private', 'member_count']
    list_filter = ['is_active', 'is_private', 'created_at']
    search_fields = ['created_by__username', 'created_by__display_name', 'name', 'description']
    readonly_fields = ['created_at']
    
    def member_count(self, obj):
        return obj.members.filter(is_active=True).count()
    member_count.short_description = 'Active Members'


@admin.register(GroupChatroomMember)
class GroupChatroomMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'group', 'role', 'joined_at', 'is_active']
    list_filter = ['role', 'is_active', 'joined_at']
    search_fields = ['user__username', 'user__display_name', 'group__name']
    readonly_fields = ['joined_at']


@admin.register(GroupMessage)
class GroupMessageAdmin(admin.ModelAdmin):
    list_display = ['author', 'group', 'content_preview', 'timestamp', 'message_type']
    list_filter = ['message_type', 'edited', 'timestamp', 'group']
    search_fields = ['author__username', 'author__display_name', 'content', 'group__name']
    readonly_fields = ['timestamp', 'edited_at']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'


@admin.register(ChatFile)
class ChatFileAdmin(admin.ModelAdmin):
    list_display = ['original_name', 'uploaded_by', 'file_size', 'uploaded_at', 'file_type']
    list_filter = ['uploaded_at', 'file_type']
    search_fields = ['original_name', 'uploaded_by__username', 'uploaded_by__display_name']
    readonly_fields = ['uploaded_at', 'file_size']


@admin.register(ChatImage)
class ChatImageAdmin(admin.ModelAdmin):
    list_display = ['original_name', 'uploaded_by', 'file_size', 'width', 'height', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['original_name', 'uploaded_by__username', 'uploaded_by__display_name']
    readonly_fields = ['uploaded_at', 'file_size', 'width', 'height']
