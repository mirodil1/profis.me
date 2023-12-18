from typing import Any

from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from rest_framework import serializers

from profis.chats.models import Chat, Message

User = get_user_model()


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = [
            "id",
            "chat_name",
            "participants",
            "created_at",
        ]


class ChatCreateSerializer(serializers.ModelSerializer):
    current_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    participant = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

    class Meta:
        model = Chat
        fields = ["current_user", "participant"]

    def create(self, validated_data: Any) -> Any:
        current_user = validated_data.get("current_user", None)
        other_user = validated_data.get("participant", None)
        chat_name = "chat_" + (
            f"{current_user.id}_{other_user.id}"
            if int(current_user.id) > int(other_user.id)
            else f"{other_user.id}_{current_user.id}"
        )
        chat, craeted = Chat.objects.get_or_create(chat_name=chat_name)
        if craeted:
            chat.participants.add(current_user, other_user)
        return chat


class MessageSerialzer(serializers.ModelSerializer):
    file = serializers.FileField(read_only=True)

    class Meta:
        model = Message
        fields = [
            "id",
            "participants",
            "sender",
            "content",
            "file",
            "is_seen",
            "created_at",
        ]


class MessageCreateSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)
    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())
    participants = serializers.PrimaryKeyRelatedField(queryset=Chat.objects.all(), write_only=True)

    class Meta:
        model = Message
        fields = [
            "participants",
            "sender",
            "file",
        ]

    def validate(self, validated_data):
        file = validated_data.get("file", None)

        if file:
            if file.size > 10485760:
                raise serializers.ValidationError(_("Допустимый размер файла 10 мб"))
        else:
            raise serializers.ValidationError(_("Это поле не может быть пустым"))
        return validated_data
