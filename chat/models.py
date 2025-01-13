import os, uuid
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

def chat_files_path(instance, filename):
    folder_name = f"chat/chat_files/{instance.room.uid}"
    return os.path.join(folder_name, filename)

def avatar_path(instance, filename):
    folder_name = f"chat/users/avatars"
    ext = filename.split('.')[-1]
    new_filename = f"avatar_{instance.user.username}.{ext}"
    return os.path.join(folder_name, new_filename)

class Profile(models.Model):
    uid = models.UUIDField(max_length=200, unique=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to=avatar_path, blank=True, null=True, default='chat/users/default/user.png')
    bio = models.TextField(blank=True, null=True)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(blank=True, null=True)

    @property
    def full_name(self):
        return self.user.get_full_name()

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = str(uuid.uuid4())

        default_avatar = 'chat/users/default/user.png'
        if self.avatar and self._avatar_needs_compression():
            if self.avatar.name != default_avatar:
                self._compress_avatar()
                
        if not self.avatar:
            self.avatar = default_avatar
        super().save(*args, **kwargs)

    def _avatar_needs_compression(self):
        """ Check if the avatar needs to be compressed (only if it has changed). """
        if not self.pk:  # New profile, avatar needs processing
            return True
        old_avatar = Profile.objects.filter(pk=self.pk).first()
        return old_avatar.avatar != self.avatar if old_avatar else True

    def _compress_avatar(self):
        """ Compress and resize the avatar image. """
        img = Image.open(self.avatar)
        img = img.convert('RGB')  # Ensure image is in RGB mode for consistent compression

        # Resize the image while maintaining the aspect ratio, ensuring neither dimension exceeds 500px
        max_size = (500, 500) # won't be exactly 500x500, it will be set as aspect ratio
        img.thumbnail(max_size, Image.LANCZOS)

        # Save the compressed image to memory
        buffer = BytesIO()
        img.save(buffer, format='JPEG', quality=100)
        buffer.seek(0)

        # Check if the image exceeds the file size limit (1 MB)
        # max_size_bytes = 1 * 1024 * 1024  # 1 MB
        # if buffer.tell() > max_size_bytes:
        #     # Apply further compression if the file size is still too large
        #     buffer = BytesIO()  # Reset the buffer
        #     img.save(buffer, format='JPEG', quality=60)  # Lower quality for more compression
        #     buffer.seek(0)

        # Replace the avatar with the resized and compressed image
        img_name = f"avatar_{self.user.username}.jpg"  # Save as JPEG with .jpg extension
        self.avatar = InMemoryUploadedFile(buffer, None, img_name, 'image/jpeg', buffer.tell(), None)

    def __str__(self):
        return self.user.username

class ChatRoom(models.Model):
    uid = models.CharField(max_length=200, unique=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    # 1) User if is_private==False, othewise NULL. 2)access all ChatRooms of a user by User.admin_of_rooms.all()
    admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='admin_of_rooms')
    # access all rooms of a user by User.rooms.all() that means if a username is anwar then anwar.rooms.all() will return all rooms of anwar
    members = models.ManyToManyField(User, blank=True, related_name='rooms')
    
    is_private = models.BooleanField(default=False)
    # I will use this field in views function, this field is not neccessary, everything will works just fine even without this field
    second_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
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
