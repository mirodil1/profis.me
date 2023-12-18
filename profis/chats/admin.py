from django.contrib import admin

from profis.chats.models import Chat, Message


class MessageInline(admin.StackedInline):
    model = Message
    extra = 5
    readonly_fields = ["pk"]


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ["chat_name"]
    inlines = [MessageInline]
