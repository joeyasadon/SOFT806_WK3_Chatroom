from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class UserProfile(AbstractUser):
    """Custom user model with additional chat-related fields"""
    display_name = models.CharField(max_length=50, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=[
        ('online', 'Online'),
        ('away', 'Away'),
        ('busy', 'Busy'),
        ('offline', 'Offline')
    ], default='offline')
    last_seen = models.DateTimeField(default=timezone.now)
    bio = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.display_name or self.username}'s profile"


class PublicChatHistory(models.Model):
    """Public chat messages visible to all users"""
    author = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='public_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    message_type = models.CharField(max_length=20, choices=[
        ('text', 'Text'),
        ('image', 'Image'),
        ('file', 'File'),
        ('system', 'System')
    ], default='text')
    reply_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.author.display_name or self.author.username}: {self.content[:50]}..."


class PrivateMessage(models.Model):
    """Private messages between two users"""
    sender = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    message_type = models.CharField(max_length=20, choices=[
        ('text', 'Text'),
        ('image', 'Image'),
        ('file', 'File')
    ], default='text')
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    reply_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['sender', 'receiver']),
            models.Index(fields=['receiver', 'is_read']),
        ]
    
    def __str__(self):
        return f"From {self.sender.display_name or self.sender.username} to {self.receiver.display_name or self.receiver.username}: {self.content[:50]}..."


class GroupChatroom(models.Model):
    """Group chat rooms with multiple participants"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='created_groups')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_private = models.BooleanField(default=False)
    max_participants = models.IntegerField(default=100)
    avatar = models.ImageField(upload_to='group_avatars/', blank=True, null=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class GroupChatroomMember(models.Model):
    """Many-to-many relationship for group chat participants"""
    group = models.ForeignKey(GroupChatroom, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='group_memberships')
    joined_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=20, choices=[
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
        ('member', 'Member')
    ], default='member')
    is_active = models.BooleanField(default=True)
    last_read_message_id = models.IntegerField(null=True, blank=True)
    
    class Meta:
        unique_together = ['group', 'user']
        indexes = [
            models.Index(fields=['group', 'is_active']),
            models.Index(fields=['user', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.user.display_name or self.user.username} in {self.group.name}"


class GroupMessage(models.Model):
    """Messages within group chat rooms"""
    group = models.ForeignKey(GroupChatroom, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='group_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    message_type = models.CharField(max_length=20, choices=[
        ('text', 'Text'),
        ('image', 'Image'),
        ('file', 'File'),
        ('system', 'System')
    ], default='text')
    reply_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['group', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.author.display_name or self.author.username} in {self.group.name}: {self.content[:50]}..."


class ChatFile(models.Model):
    """Files shared in chat (images, documents, etc.)"""
    file = models.FileField(upload_to='chat_files/')
    original_name = models.CharField(max_length=255)
    file_size = models.BigIntegerField()
    file_type = models.CharField(max_length=100)
    uploaded_by = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # Optional: Link to specific message where file was shared
    public_message = models.ForeignKey(PublicChatHistory, on_delete=models.SET_NULL, null=True, blank=True, related_name='files')
    private_message = models.ForeignKey(PrivateMessage, on_delete=models.SET_NULL, null=True, blank=True, related_name='files')
    group_message = models.ForeignKey(GroupMessage, on_delete=models.SET_NULL, null=True, blank=True, related_name='files')
    
    class Meta:
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['uploaded_by', 'uploaded_at']),
        ]
    
    def __str__(self):
        return f"{self.original_name} uploaded by {self.uploaded_by.display_name or self.uploaded_by.username}"


class ChatImage(models.Model):
    """Images shared in chat (separate from files for better handling)"""
    image = models.ImageField(upload_to='chat_images/')
    original_name = models.CharField(max_length=255)
    file_size = models.BigIntegerField()
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    uploaded_by = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # Optional: Link to specific message where image was shared
    public_message = models.ForeignKey(PublicChatHistory, on_delete=models.SET_NULL, null=True, blank=True, related_name='images')
    private_message = models.ForeignKey(PrivateMessage, on_delete=models.SET_NULL, null=True, blank=True, related_name='images')
    group_message = models.ForeignKey(GroupMessage, on_delete=models.SET_NULL, null=True, blank=True, related_name='images')
    
    class Meta:
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['uploaded_by', 'uploaded_at']),
        ]
    
    def __str__(self):
        return f"{self.original_name} uploaded by {self.uploaded_by.display_name or self.uploaded_by.username}"
