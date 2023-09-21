from django.urls import path

from profis.categories.views import CategoryListViewSet

app_name = "categories"

urlpatterns = [
    path("", CategoryListViewSet.as_view({"get": "list"}), name="list"),
]
