import pytest
from rest_framework.test import APIRequestFactory

from profis.users.models import User
from profis.users.views import UserViewSet


class TestUserViewSet:
    @pytest.fixture
    def api_rf(self) -> APIRequestFactory:
        return APIRequestFactory()

    def test_get_queryset(self, user: User, api_rf: APIRequestFactory):
        view = UserViewSet()
        request = api_rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert user in view.get_queryset()

    def test_me(self, user: User, api_rf: APIRequestFactory):
        view = UserViewSet()
        request = api_rf.get("/fake-url/")
        request.user = user

        view.request = request

        response = view.me(request)  # type: ignore

        assert response.data == {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "bio": user.bio,
            "email": user.email,
            "age": user.age,
            "avatar": "http://testserver" + user.avatar.url,
            "number_of_views": user.number_of_views,
            "is_worker": user.is_worker,
            "work_experiance": user.work_experiance,
            "gender": user.gender,
        }
