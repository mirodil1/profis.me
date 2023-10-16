from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, validators
from rest_framework.exceptions import ValidationError

from profis.ratings.models import TaskRating
from profis.tasks.models import Task


class WorkerTaskRatingSerializer(serializers.ModelSerializer):
    worker = serializers.SerializerMethodField()
    task = serializers.SerializerMethodField()

    class Meta:
        model = TaskRating
        fields = [
            "worker",
            "task",
            "politeness",
            "punctuality",
            "adequacy",
            "review",
            "created_at",
        ]

    def get_worker(self, obj):
        worker = obj.task.worker
        return {"id": worker.id, "first_name": worker.first_name, "last_name": worker.last_name}

    def get_task(self, obj):
        task = obj.task
        return {"id": task.id, "name": task.name}


class OrdererTaskRatingSerializer(serializers.ModelSerializer):
    orderer = serializers.SerializerMethodField()
    task = serializers.SerializerMethodField()

    class Meta:
        model = TaskRating
        fields = [
            "orderer",
            "task",
            "politeness",
            "quality",
            "cost_of_services",
            "review",
            "created_at",
        ]

    def get_orderer(self, obj):
        orderer = obj.task.owner
        return {"id": orderer.id, "first_name": orderer.first_name, "last_name": orderer.last_name}

    def get_task(self, obj):
        task = obj.task
        return {"id": task.id, "name": task.name}


class WorkerTaskRatingCreateSerializer(serializers.ModelSerializer):
    worker = serializers.HiddenField(default=serializers.CurrentUserDefault())
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), write_only=True)

    class Meta:
        model = TaskRating
        validators = [
            validators.UniqueTogetherValidator(
                queryset=TaskRating.objects.all(),
                fields=["worker", "task"],
                message=_("The fields worker and task must be a unique set."),
            )
        ]
        fields = [
            "worker",
            "task",
            "politeness",
            "punctuality",
            "adequacy",
            "review",
        ]

    def validate(self, data):
        worker = data.get("worker")
        task = data.get("task")

        # Check if the worker is the same as the orderer (owner of the task)
        if worker == task.owner:
            raise ValidationError(_("Вы не можете оценивать себя как исполнителя."))

        return data


class OrdererTaskRatingCreateSerializer(serializers.ModelSerializer):
    orderer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), write_only=True)

    class Meta:
        model = TaskRating
        validators = [
            validators.UniqueTogetherValidator(
                queryset=TaskRating.objects.all(),
                fields=["orderer", "task"],
                message=_("The fields orderer and task must be a unique set."),
            )
        ]
        fields = [
            "orderer",
            "task",
            "politeness",
            "quality",
            "cost_of_services",
            "review",
        ]
