from django.urls import path

from profis.chats.consumers import ChatConsumer

websocket_urlpatterns = [
    path("ws/chat/<int:id>", ChatConsumer.as_asgi()),
]
