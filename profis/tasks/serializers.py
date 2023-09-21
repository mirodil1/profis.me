from rest_framework import serializers

from profis.categories.models import Category
from profis.categories.serializers import CategorySerializer
from profis.tasks.models import Task, TaskImage


class TaskImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskImage
        fields = [
            "id",
            "image",
        ]


class TaskSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    file = serializers.FileField(read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "category",
            "owner",
            "name",
            "description",
            "phone_number",
            "file",
            "status",
            "start_time",
            "finish_time",
            "number_of_views",
        ]


class TaskCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), source="category", write_only=True)
    file = serializers.FileField(write_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000, allow_empty_file=False, use_url=False), write_only=True
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "category",
            "name",
            "description",
            "phone_number",
            "file",
            "uploaded_images",
            "start_time",
            "finish_time",
        ]

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        task = Task.objects.create(**validated_data)
        for image in uploaded_images:
            TaskImage.objects.create(task=task, image=image)
        return task
