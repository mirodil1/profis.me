from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.db.models import Count, F
from django_filters import rest_framework as filters

from profis.tasks.models import Task


class TaskFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="budget", lookup_expr="gte")
    no_response = filters.BooleanFilter(method="filter_by_response")
    point = filters.CharFilter(method="filter_by_distance")

    class Meta:
        model = Task
        fields = ["is_remote", "is_business", "category__child", "no_response"]

    def filter_by_distance(self, queryset, name, value):
        point = value.split(",")
        if len(point) == 2:
            try:
                latitude = float(point[0])
                longitude = float(point[1])
                pnt = Point(latitude, longitude, srid=4326)
                query_distance = float(self.data.get("distance")) * 1000

                queryset = (
                    queryset.annotate(distance=Distance(F("address__coords"), pnt)).order_by("id").distinct("id")
                )
                queryset = queryset.filter(distance__lte=query_distance)
            except Exception:
                pass
        return queryset

    def filter_by_response(self, queryset, name, value):
        if value:
            queryset = queryset.annotate(response_count=Count("responses"))
            # Filter tasks where the response count is zero
            queryset = queryset.filter(response_count=0)
        return queryset
