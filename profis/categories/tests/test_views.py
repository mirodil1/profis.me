import pytest
from rest_framework.test import APIRequestFactory

from profis.categories.models import Category
from profis.categories.views import CategoryListViewSet


class TestUserViewSet:
    @pytest.fixture
    def api_rf(self) -> APIRequestFactory:
        return APIRequestFactory()

    def test_get_queryset(self, category: Category, api_rf: APIRequestFactory):
        view = CategoryListViewSet()
        request = api_rf.get("/fake-url/")
        view.request = request
        print(view)
        assert category in view.get_queryset()
