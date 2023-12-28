from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Called when a WebSocket connection is opened.
        """
        user = self.scope["user"]
        if user.is_authenticated:
            await self.accept()
            await self.update_user_status(user_id=user.id, status=1)

    async def disconnect(self, code):
        user = self.scope["user"]
        await self.update_user_status(user_id=user.id, status=0)
        await self.update_user_last_seen(user.id)

    @database_sync_to_async
    def update_user_status(self, user_id, status):
        """
        Update user online status
        """
        User.objects.filter(id=user_id).update(online_status=status)

    @database_sync_to_async
    def update_user_last_seen(self, user_id):
        """
        Update user last online state
        """
        User.objects.filter(id=user_id).update(last_seen=timezone.now())
