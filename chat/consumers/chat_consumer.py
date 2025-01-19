import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import ChatRoom, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        # Close connection if user is unauthenticated
        self.user = self.scope['user']
        if not self.user.is_authenticated:
            await self.close()
            return

        # Get the room uid from the URL
        self.room_uid = self.scope['url_route']['kwargs']['room_uid']
        self.room_group_name = f'chat_{self.room_uid}'

        # Storing variables to use in other functions to reduce db query
        self.profile = await database_sync_to_async(lambda: getattr(self.user, 'profile', None))()
        self.chat_room = await database_sync_to_async(lambda: ChatRoom.objects.filter(uid=self.room_uid).first())()

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
            await database_sync_to_async(lambda: Message.objects.create(
                room=self.chat_room, author=self.user, content=message))()

        # Broadcast to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'sendMessage',
                'msgType': msgType,
                'content': message,
                'author': self.user.username,
                'author_name': self.profile.full_name,
                'avatar': self.profile.avatar.url,
                'is_private_room': self.chat_room.is_private
            }
        )
    
    async def sendMessage(self, event):
        await self.send(text_data=json.dumps(event))