from django.db.models.query import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from profis.ratings.models import TaskRating
from profis.ratings.serializers import TaskRatingCreateSerializer, TaskRatingSerializer
from profis.tasks.models import Task


@extend_schema(tags=["ratings"], description="<h3><li>Get list of ratings for requested user</li><h3>")
class TaskRatingViewSet(ListModelMixin, GenericViewSet):
    serializer_class = TaskRatingSerializer
    queryset = TaskRating.objects.all()

    def get_queryset(self) -> QuerySet:
        """
        Returns ratings for specified user
        """
        qs = super().get_queryset()
        user_id = self.kwargs["user_id"]
        return qs.filter(worker=user_id).select_related("task", "task__worker")


@extend_schema(tags=["ratings"], description="<h3><li>Rate the worker after the task has finished</li><h3>")
class TaskRatingCreateViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = TaskRatingCreateSerializer
    queryset = TaskRating.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task_rating = serializer.save()
        headers = self.get_success_headers(serializer.data)

        # Update status of the task
        task = task_rating.task
        task.status = Task.Status.COMPLETED
        task.save()

        print(task.status)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
