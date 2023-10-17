from django.contrib import admin

from profis.tasks.models import Task, TaskAddress, TaskImage, TaskResponse


class TaskResponseInline(admin.StackedInline):
    model = TaskResponse
    extra = 2


class TaskAddressInline(admin.StackedInline):
    model = TaskAddress
    extra = 2


class TaskImageInline(admin.StackedInline):
    model = TaskImage
    extra = 2


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "category",
        "owner",
        "status",
        "number_of_views",
    ]
    list_filter = [
        "status",
        "created_at",
    ]
    search_fields = [
        "name",
        "description",
    ]
    readonly_fields = [
        "number_of_views",
        "owner",
    ]
    inlines = [TaskImageInline, TaskAddressInline, TaskResponseInline]
