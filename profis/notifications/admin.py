from django.contrib import admin

from profis.notifications.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["notification_type", "is_read"]
