import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from profis.notifications.models import Notification


@receiver(post_save, sender=Notification)
def send_notification(sender, instance, created, **kwargs):
    """
    Send notification by type
    """
    if created:
        # Getting number of unread notifications
        notification_count = (
            Notification.objects.filter(is_read=False, user=instance.user)
            .exclude(notification_type=Notification.NotificationType.MESSAGE)
            .count()
        )
        data = {"count": notification_count}
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"notification_{instance.user.id}",
            {
                "type": "send_notification",
                "value": json.dumps(data),
            },
        )

        # group_send(
        #     group=f"notification_{instance.user.id}",
        #     type="send_notification",
        #     data=json.dumps(data),
        # )

        # if instance.notification_type == Notification.NotificationType.MESSAGE:
        #     Chat.objects.filter(
        #         ~Q(message__sender=instance.user),
        #         message__is_seen=False,
        #         participants__user=user,
        #     )
        #     # Getting count of unread message notifications
        #     chat_notification_count = Notification.objects.filter(
        #         is_read=False,
        #         user=instance.user,
        #         notification_type=Notification.NotificationType.MESSAGE,
        #     ).count()
        #     data = {"count": chat_notification_count}
        #     group_send(
        #         group=f"chat_{instance.user.id}",
        #         type="send_chat_notification",
        #         data=json.dumps(data),
        #     )
        # else:
        #     # Getting count of unread notifications
        #     notification_count = (
        #         Notification.objects.filter(is_read=False, user=instance.user)
        #         .exclude(notification_type=Notification.NotificationType.MESSAGE)
        #         .count()
        #     )
        #     data = {"count": notification_count}
        #     group_send(
        #         group=f"notification_{instance.user.id}",
        #         type="send_notification",
        #         data=json.dumps(data),
        #     )


def group_send(group, type, data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group,
        {
            "type:": type,
            "value": data,
        },
    )
