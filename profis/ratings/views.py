from django.db.models.query import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from profis.ratings.models import TaskRating
from profis.ratings.serializers import (
    OrdererTaskRatingCreateSerializer,
    OrdererTaskRatingSerializer,
    WorkerTaskRatingCreateSerializer,
    WorkerTaskRatingSerializer,
)


@extend_schema(tags=["ratings"])
class WorkerTaskRatingViewSet(ListModelMixin, GenericViewSet):
    serializer_class = WorkerTaskRatingSerializer
    queryset = TaskRating.objects.all()

    def get_queryset(self) -> QuerySet:
        """
        Returns ratings from workers related to the requested user when they are owner of tasks
        """
        qs = super().get_queryset()
        user_id = self.kwargs["user_id"]
        return qs.filter(task__owner__id=user_id).exclude(orderer__isnull=True).select_related("task", "task__owner")


@extend_schema(tags=["ratings"])
class OrdererTaskRatingViewSet(ListModelMixin, GenericViewSet):
    serializer_class = OrdererTaskRatingSerializer
    queryset = TaskRating.objects.all()

    def get_queryset(self) -> QuerySet:
        """
        Returns ratings from orderers related to the requested user when they are worker of tasks
        """
        qs = super().get_queryset()
        user_id = self.kwargs["user_id"]
        return qs.filter(task__worker__id=user_id).exclude(worker__isnull=True).select_related("task", "task__owner")


@extend_schema(tags=["ratings"], description="<h3><li>Orderer rate the worker after the task has finished</li><h3>")
class WorkerTaskRatingCreateViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = WorkerTaskRatingCreateSerializer
    queryset = TaskRating.objects.all()


@extend_schema(tags=["ratings"], description="<h3><li>Orderer rate the worker after the task has finished</li><h3>")
class OrdererTaskRatingCreateViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = OrdererTaskRatingCreateSerializer
    queryset = TaskRating.objects.all()
