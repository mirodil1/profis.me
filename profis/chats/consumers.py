import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

from profis.chats.models import Chat, Message

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    groups = ["broadcast"]

    async def connect(self):
        # Called on connection.
        user = self.scope["user"]
        if user.is_authenticated:
            current_user_id = user.id
            other_user_id = self.scope["url_route"]["kwargs"]["id"]
            self.room_name = (
                f"{current_user_id}_{other_user_id}"
                if int(current_user_id) > int(other_user_id)
                else f"{other_user_id}_{current_user_id}"
            )
            self.room_group_name = f"chat_{self.room_name}"
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
        else:
            await self.accept()
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "websocket.close",
                        "code": 4401,  # Custom code for unauthorized
                        "text": "Unauthorized",
                    }
                )
            )
            await self.close()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        content = data.get("content", None)
        sender_id = data.get("sender", None)
        if content and sender_id:
            sender = await self.get_user(user_id=sender_id)
            chat = await self.get_chat(chat_name=self.room_group_name)
            await self.create_message(sender=sender, content=content, chat=chat)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": content,
                    "sender": sender.first_name,
                },
            )
        else:
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "websocket.close",
                        "code": 1007,
                        "text": "Unsupported payload",
                    }
                )
            )

    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        file = event["file"]
        await self.send(
            text_data=json.dumps(
                {
                    "file": file if file else None,
                    "message": message if message else None,
                    "sender": sender,
                }
            )
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_layer)
        await self.disconnect(close_code)

    @database_sync_to_async
    def get_chat(self, chat_name):
        return Chat.objects.get(chat_name=chat_name)

    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.filter(id=user_id).first()

    # @database_sync_to_async
    # def get_messages(self):
    #     chat = Chat.objects.get(chat_name=self.room_group_name)

    @database_sync_to_async
    def create_message(self, sender, content, chat):
        Message.objects.create(sender=sender, content=content, participants=chat)
