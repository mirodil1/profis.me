from django.urls import path

from profis.users.consumers import OnlineStatusConsumer

websocket_urlpatterns = [
    path("ws/user-status/", OnlineStatusConsumer.as_asgi()),
]
