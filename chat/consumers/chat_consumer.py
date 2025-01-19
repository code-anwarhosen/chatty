import json
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import ChatRoom, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the room uid from the URL
        self.room_uid = self.scope['url_route']['kwargs']['room_uid']
        self.room_group_name = f'chat_{self.room_uid}'

        # Storing variables to use in other functions to reduce db query
        self.user = self.scope['user']
        
        # Fetch user profile
        self.profile = await database_sync_to_async(lambda: getattr(self.user, 'profile', None))()

        # Fetch the chat room
        try:
            self.chat_room = await database_sync_to_async(ChatRoom.objects.get)(uid=self.room_uid)
        except ChatRoom.DoesNotExist:
            self.chat_room = None

        # Validate if the chat room exists and the user is part of it
        if not self.chat_room or not await database_sync_to_async(self.chat_room.members.filter(id=self.user.id).exists)():
            await self.close()
            return

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        msgType = data['msgType']
        message = data['content']

        if msgType == 'text':
            await self.save_message(message)

        # Broadcast to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'sendMessage',
                'msgType': msgType,
                'content': message,
                'author': self.user.username,
                'avatar': self.profile.avatar.url,
                'is_private': self.chat_room.is_private
            }
        )
    
    async def sendMessage(self, event):
        msg_type = event['msgType']
        message = event['content']
        author = event['author']
        avatar = event['avatar']
        is_private = event['is_private']

        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({
            'msgType': msg_type,
            'content': message,
            'author': author,
            'avatar': avatar,
            'is_private_room': is_private,
        }))
    
    @database_sync_to_async
    def save_message(self, message):
        room = ChatRoom.objects.get(uid=self.room_uid)
        Message.objects.create(room=room, author=self.user, content=message)
