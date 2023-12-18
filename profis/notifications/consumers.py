import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import Q

from profis.chats.models import Chat, Message
from profis.notifications.models import Notification


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Called on connection.
        user = self.scope["user"]
        if user.is_authenticated:
            current_user_id = user.id
            self.room_name = current_user_id
            self.room_group_name = f"notification_{self.room_name}"
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
            await self.group_send()

    async def disconnect(self, code):
        user = self.scope["user"]
        if user.is_authenticated:
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def group_send(self):
        notification_count = await self.count_notification(self.scope["user"])
        data = {"count": notification_count}
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "send_notification",
                "value": json.dumps(data),
            },
        )

    async def send_notification(self, event):
        data = json.loads(event.get("value"))
        count = data["count"]
        await self.send(text_data=json.dumps({"count": count}))

    @database_sync_to_async
    def count_notification(self, user):
        """
        Return number of unread notifications for the current user
        """
        return (
            Notification.objects.filter(is_read=False, user=user)
            .exclude(notification_type=Notification.NotificationType.MESSAGE)
            .count()
        )


class ChatNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Called on connection.
        user = self.scope["user"]
        if user.is_authenticated:
            current_user_id = user.id
            self.room_name = current_user_id
            self.room_group_name = f"chat_notification_{self.room_name}"
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
            await self.group_send()

    async def disconnect(self, code):
        user = self.scope["user"]
        if user.is_authenticated:
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def group_send(self):
        unread_messages = await self.count_unread_chats(self.scope["user"])
        data = {"count": unread_messages}
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "send_notification",
                "value": json.dumps(data),
            },
        )

    async def send_notification(self, event):
        data = json.loads(event.get("value"))
        count = data["count"]
        await self.send(text_data=json.dumps({"count": count}))

    @database_sync_to_async
    def count_unread_chats(self, user):
        """
        Return number of chats which has unread messages
        """
        return Message.objects.filter(
            ~Q(sender=user),
            is_seen=False,
            participants__in=Chat.objects.filter(participants=user),
        ).count()
