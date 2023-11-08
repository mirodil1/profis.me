from typing import Any

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils.translation import gettext as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from profis.chats.models import Chat, Message
from profis.chats.serializers import ChatCreateSerializer, ChatSerializer, MessageCreateSerializer, MessageSerialzer


@extend_schema(tags=["chats"])
class ChatListViewSet(ListModelMixin, GenericViewSet):
    serializer_class = ChatSerializer
    queryset = Chat.objects.all().prefetch_related()


@extend_schema(tags=["chats"])
class ChatCreateViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = ChatCreateSerializer
    queryset = Chat.objects.all().prefetch_related()

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        chat = serializer.save()
        headers = self.get_success_headers(serializer.data)

        return self.response_data(chat=chat, headers=headers)

    def response_data(self, chat: Chat, headers) -> dict[str, Any]:
        """
        Custom response data for ChatViewSet
        """
        try:
            _response = {
                "id": chat.id,
                "chat_name": chat.chat_name,
                "participants": [
                    {
                        "id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                    }
                    for user in chat.participants.all()
                ],
                "messages": [
                    {
                        "id": message.id,
                        "sender": {
                            "id": message.sender.id,
                            "full_name": message.sender.first_name,
                            "last_name": message.sender.last_name,
                        },
                        "content": message.content if message.content else None,
                        "file": message.file.path if message.file else None,
                        "is_seen": message.is_seen,
                        "created_at": message.created_at,
                    }
                    for message in Message.objects.filter(participants=chat)
                    .select_related("sender")
                    .order_by("-created_at")
                ],
            }
            return Response(_response, status=status.HTTP_200_OK, headers=headers)
        except Exception as e:
            _response = {"error": _(str(e))}
            return Response(_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR, headers=headers)


@extend_schema(tags=["chats"])
class MessageListViewSet(ListModelMixin, GenericViewSet):
    serializer_class = MessageSerialzer
    queryset = Message.objects.all()


@extend_schema(tags=["chats"])
class MessageCreateViewSet(CreateModelMixin, GenericViewSet):
    """
    Use this only for uploading (sending) files, for sending messages use websocket
    """

    serializer_class = MessageCreateSerializer
    queryset = Message.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        headers = self.get_success_headers(serializer.data)
        channel_layer = get_channel_layer()
        chat_name = message.participants.chat_name

        async_to_sync(channel_layer.group_send)(
            chat_name,
            {
                "type": "chat_message",
                "id": message.id,
                "file": request.build_absolute_uri(message.file.url),
                "message": None,
                "sender": message.sender.first_name,
            },
        )
        response = {
            "id": message.id,
            "file": request.build_absolute_uri(message.file.url),
            "sender": message.sender.first_name,
        }

        return Response(response, status=status.HTTP_200_OK, headers=headers)
