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
            }
        )
    
    async def sendMessage(self, event):
        msg_type = event['msgType']
        message = event['content']
        author = event['author']
        avatar = event['avatar']

        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({
            'msgType': msg_type,
            'content': message,
            'author': author,
            'avatar': avatar,
        }))
    
    @database_sync_to_async
    def save_message(self, message):
        room = ChatRoom.objects.get(uid=self.room_uid)
        Message.objects.create(room=room, author=self.user, content=message)
