from django.urls import path

from profis.subscription.views import UserPlanCreateViewSet, UserPlanListViewSet

app_name = "subscriptions"

urlpatterns = [
    path("", UserPlanListViewSet.as_view({"get": "list"}, name="list")),
    path("plan/purchase/", UserPlanCreateViewSet.as_view({"post": "create"}, name="create")),
]
