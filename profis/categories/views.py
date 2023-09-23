from drf_spectacular.utils import extend_schema
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from profis.categories.models import Category
from profis.categories.serializers import CategorySerializer


@extend_schema(tags=["categories"])
class CategoryListViewSet(ListModelMixin, GenericViewSet):
    queryset = Category.objects.filter(parent_category=None)
    serializer_class = CategorySerializer
