import uuid
from django.db import models
from django.contrib.auth.models import User

class ChatRoom(models.Model):
    uid = models.CharField(max_length=200, unique=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    members = models.ManyToManyField(User, blank=True, related_name='rooms') # access all rooms of a user by user.rooms.all() that means if a username is anwar then anwar.rooms.all() will return all rooms of anwar
    is_private = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-updated_at', 'created_at')

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = str(uuid.uuid4())
        super().save(*args, **kwargs)
    
    def __str__(self):
        if self.is_private:
            return f"Private chat between {self.members.all().first()} and {self.members.all().last()}"
        return f"Group: {self.name}"
    

class Message(models.Model):
    MESSAGE_TYPE_CHOICES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('file', 'File'),
    ]
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages') # access all messages of a room by room.messages.all() that means if a room name is 'room1' then room1.messages.all() will return all messages of room1
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages') # access all messages sent by a user by user.sent_messages.all() that means if a username is anwar then anwar.sent_messages.all() will return all messages sent by anwar
    content = models.CharField(max_length=300, blank=True, null=True)
    file = models.FileField(upload_to='uploads/', blank=True, null=True)
    type = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES, default='text')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        if self.type == 'text':
            return f"{self.author.username}: {self.content[:30]}"
        return f"{self.author.username}: {self.type} message"

class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)

    is_admin = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'room')

    def __str__(self):
        return f"{self.user.username} in {self.room.name}"
