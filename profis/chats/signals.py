import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver

from profis.chats.models import Chat, Message


@receiver(post_save, sender=Message)
def send_notification(sender, instance, created, **kwargs):
    """
    Send number of unread messages
    """
    if created:
        chat = instance.participants
        participant = chat.participants.get(~Q(id=instance.sender.id))

        # Getting number of messages
        messages_count = Message.objects.filter(
            ~Q(sender=participant),
            is_seen=False,
            participants__in=Chat.objects.filter(participants=participant),
        ).count()
        data = {"count": messages_count}
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_notification_{participant.id}",
            {
                "type": "send_notification",
                "value": json.dumps(data),
            },
        )
