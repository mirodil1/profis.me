from django.urls import path

from profis.categories.views import CategoryBaseListViewSet, CategoryListViewSet, CategoryUnlimListViewSet

app_name = "categories"

urlpatterns = [
    path("", CategoryListViewSet.as_view({"get": "list"}), name="list"),
    path("plan/unlim/", CategoryUnlimListViewSet.as_view({"get": "list"}), name="unlim-list"),
    path("plan/base/", CategoryBaseListViewSet.as_view({"get": "list"}), name="base-list"),
]
