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
        fields = [
            "id",
            "name",
            "icon",
            "price",
            "slug",
            "child",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data["child"] == []:
            del data["child"]
        return data


class CategoryUnlimSerializer(CategorySerializer):
    """
    Categories including unlim package fields
    """

    class Meta:
        model = Category
        fields = [field for field in CategorySerializer.Meta.fields] + [
            "unlim_price_15",
            "unlim_price_30",
            "unlim_price_90",
        ]


class CategoryBaseSerializer(serializers.ModelSerializer):
    """
    Categories including base package fields
    """

    class Meta:
        model = Category
        fields = [field for field in CategorySerializer.Meta.fields if field != "child"] + [
            "base_price_25",
            "base_price_50",
            "base_price_100",
        ]
