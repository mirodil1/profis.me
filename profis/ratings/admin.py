from django.contrib import admin

from profis.ratings.models import TaskRating


@admin.register(TaskRating)
class TaskRatingAdmin(admin.ModelAdmin):
    list_display = ["task"]
