from rest_framework import serializers

from profis.categories.models import Category
from profis.categories.serializers import CategorySerializer
from profis.tasks.models import Task, TaskImage
from profis.users.serializers import UserSerializer


class TaskImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskImage
        fields = [
            "id",
            "image",
        ]


class TaskSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    owner = UserSerializer()
    file = serializers.FileField(read_only=True)
    images = TaskImageSerializer(many=True)

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
            "images",
            "number_of_views",
        ]


class TaskCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)
    file = serializers.FileField(write_only=True, required=False)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False,
    )
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

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
            "uploaded_images",
            "start_time",
            "finish_time",
        ]

    def create(self, validated_data):
        uploaded_images = validated_data.get("uploaded_images", None)
        task = Task.objects.create(**validated_data)
        if uploaded_images:
            for image in uploaded_images:
                TaskImage.objects.create(task=task, image=image)
        return task
