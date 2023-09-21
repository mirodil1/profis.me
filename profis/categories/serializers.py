from rest_framework import serializers

from profis.categories.models import Category


class RecursiveField(serializers.Serializer):
    """
    Get categories field children recursively
    """

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CategorySerializer(serializers.ModelSerializer):
    child = RecursiveField(many=True)

    class Meta:
        model = Category
        fields = ["id", "name", "icon", "slug", "child"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        print(data)
        if data["child"] == []:
            del data["child"]
        return data
