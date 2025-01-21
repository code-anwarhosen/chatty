from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'online-status'

        self.user = self.scope['user']
        self.profile = await database_sync_to_async(lambda: getattr(self.user, 'profile', None))()
        
        if not self.user.is_authenticated or not self.profile:
            await self.close()
            return

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # Check if user is already marked online to avoid redundant updates
        if not self.profile.is_online:
            await database_sync_to_async(self.setOnlineStatus)(True)

            # Notify other users only if the status was actually changed
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "sendOnlineStatus",
                    "username": self.user.username,
                    "is_online": True,
                    "last_seen": str(self.profile.last_seen),
                },
            )

    async def disconnect(self, close_code):
        # Only update offline status if the user was marked online
        if self.profile and self.profile.is_online:
            await database_sync_to_async(self.setOnlineStatus)(False)

            # Notify other users
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "sendOnlineStatus",
                    "username": self.user.username,
                    "is_online": False,
                    "last_seen": str(self.profile.last_seen),
                },
            )

        # Leave the group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)


    def setOnlineStatus(self, status=True):
        if self.profile:  # Ensure profile exists before setting the status
            self.profile.is_online = status
            self.profile.save(update_fields=['is_online'])

    async def sendOnlineStatus(self, event):
        await self.send(text_data=json.dumps(event))
