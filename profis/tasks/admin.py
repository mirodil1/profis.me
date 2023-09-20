from django.contrib import admin

from profis.tasks.models import Task, TaskImage


class TaskImageInline(admin.StackedInline):
    model = TaskImage
    extra = 5


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
    inlines = [
        TaskImageInline,
    ]
