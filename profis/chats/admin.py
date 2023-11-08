from django.contrib import admin

from profis.chats.models import Chat


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ["chat_name"]
