from django.contrib.auth import get_user_model
from rest_framework import serializers

from profis.users.models import User as UserType

User = get_user_model()


class UserSerializer(serializers.ModelSerializer[UserType]):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]
