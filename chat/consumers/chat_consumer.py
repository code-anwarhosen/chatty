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
        self.profile = await database_sync_to_async(lambda: self.user.profile)()

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
        message = data['message']
        await self.save_message(message)

        # Broadcast the message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'message_type': 'text' if message else 'image',
                'author': self.user.username,
                'avatar': self.profile.avatar.url
            }
        )
    
    @database_sync_to_async
    def save_message(self, message):
        room = ChatRoom.objects.get(uid=self.room_uid)
        Message.objects.create(room=room, author=self.user, content=message)

    async def chat_message(self, event):
        message = event['message']
        message_type = event['message_type']
        author = event['author']
        avatar = event['avatar']

        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'message_type': message_type,
            'author': author,
            'avatar': avatar,
        }))
