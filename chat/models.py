from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.models import User
from django.db import models
from io import BytesIO
from PIL import Image
import os, uuid

default_user_avatar = 'chat/avatars/users/default/user.png'
default_group_avatar = 'chat/avatars/groups/default/group.png'

def chat_files_path(instance, filename):
    folder_name = f"chat/files/{instance.room.uid}"
    return os.path.join(folder_name, filename)

def user_avatar_path(instance, filename):
    folder_name = f"chat/avatars/users"
    ext = filename.split('.')[-1]
    new_filename = f"avatar_{instance.user.username}.{ext}"
    return os.path.join(folder_name, new_filename)

def chat_group_avatar_path(instance, filename):
    folder_name = f"chat/avatars/groups"
    ext = filename.split('.')[-1]

    group_name = str(instance.name).replace(' ', '_')
    new_filename = f"avatar_{group_name}.{ext}"
    return os.path.join(folder_name, new_filename)

def compress_avatar(image):
    """Compress and resize the image to ensure it doesn't exceed the size limit."""
    img = Image.open(image)
    img = img.convert('RGB')  # Ensure consistent compression format

    # Resize the image while maintaining aspect ratio, max dimensions 500x500
    max_size = (500, 500)
    img.thumbnail(max_size, Image.LANCZOS)

    # Save the compressed image to memory
    buffer = BytesIO()
    img.save(buffer, format='JPEG', quality=90)
    buffer.seek(0)

    # Return the new compressed image
    return InMemoryUploadedFile(buffer, None, image.name, 'image/jpeg', buffer.tell(), None)

class Profile(models.Model):
    uid = models.UUIDField(max_length=200, unique=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True)
    bio = models.TextField(blank=True, null=True)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('user',)

    @property
    def full_name(self):
        return self.user.get_full_name()

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = str(uuid.uuid4())

        if self.avatar and self._avatar_needs_compression():
            if self.avatar.name != default_user_avatar:
                self.avatar = compress_avatar(self.avatar)
                
        if not self.avatar:
            self.avatar = default_user_avatar
        super().save(*args, **kwargs)

    def _avatar_needs_compression(self):
        """ Check if the avatar needs to be compressed (only if it has changed). """
        if not self.pk:  # New profile, avatar needs processing
            return True
        old_avatar = Profile.objects.filter(pk=self.pk).first()
        return old_avatar.avatar != self.avatar if old_avatar else True

    def __str__(self):
        return self.user.username

class ChatRoom(models.Model):
    uid = models.CharField(max_length=200, unique=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    avatar = models.ImageField(upload_to=chat_group_avatar_path, blank=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='admin_of_rooms') # access all ChatRooms of a user by User.admin_of_rooms.all()
    members = models.ManyToManyField(User, blank=True, related_name='rooms') # access all rooms of a user by User.rooms.all()
    
    is_private = models.BooleanField(default=False)
    second_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True) # I will use this field in views function for storing second_user for private chat
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-updated_at', 'created_at')

    @property
    def member_count(self):
        return self.members.count()

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = str(uuid.uuid4())

        if self.admin:
            self.is_private = False

        if self.avatar and self._avatar_needs_compression():
            if self.avatar.name != default_group_avatar:
                self.avatar = compress_avatar(self.avatar)

        if not self.avatar and not self.is_private:
            self.avatar = default_group_avatar
        super().save(*args, **kwargs)

    def _avatar_needs_compression(self):
        """Check if the avatar needs to be compressed."""
        if not self.pk:
            return True
        old_avatar = ChatRoom.objects.filter(pk=self.pk).first()
        return old_avatar.avatar != self.avatar if old_avatar else True
    
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
    file = models.FileField(upload_to=chat_files_path, blank=True, null=True)
    type = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES, default='text')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        if self.type == 'text':
            return f"{self.author.username}: {self.content[:30]}"
        return f"{self.author.username}: {self.type} message"
