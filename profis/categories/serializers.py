from parler_rest.fields import TranslatedFieldsField
from parler_rest.serializers import TranslatableModelSerializer
from rest_framework import serializers

from profis.categories.models import Category
from profis.utils.serializers import TranslatedSerializerMixin


class RecursiveField(serializers.Serializer):
    """
    Get categories field children recursively
    """

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CategorySerializer(TranslatedSerializerMixin, TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Category)
    child = RecursiveField(many=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "translations",
            "icon",
            "price",
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


class CategoryBaseSerializer(TranslatedSerializerMixin, TranslatableModelSerializer):
    """
    Categories including base package fields
    """

    translations = TranslatedFieldsField(shared_model=Category)

    class Meta:
        model = Category
        fields = [
            "translations",
            "base_price_25",
            "base_price_50",
            "base_price_100",
        ]
