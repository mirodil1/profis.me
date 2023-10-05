from rest_framework import serializers

from profis.ratings.models import TaskRating


class WorkerTaskRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskRating
        fields = [
            "id",
            "worker",
            "politeness",
            "punctuality",
            "adequacy",
            "review",
            "created_at",
        ]
