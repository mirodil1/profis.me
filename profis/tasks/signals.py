from django.db.models.signals import post_save
from django.dispatch import receiver

from profis.notifications.models import Notification
from profis.tasks.models import TaskResponse


@receiver(post_save, sender=TaskResponse)
def create_notification(sender, instance, created, **kwargs):
    """
    Create notification when new response is created for task
    """
    if created:
        Notification.objects.create(
            notification_type=Notification.NotificationType.RESPONSE,
            content_type=TaskResponse,
            object_id=instance.id,
            user=instance.task.owner,
        )
