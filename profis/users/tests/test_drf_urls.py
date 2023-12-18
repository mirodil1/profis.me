from django.urls import resolve, reverse

from profis.users.models import User


def test_user_detail(user: User):
    assert reverse("users:detail", kwargs={"id": user.id}) == f"/ru/api/users/{user.id}/"
    assert resolve(f"/ru/api/users/{user.pk}/").view_name == "users:detail"


def test_user_list():
    assert reverse("users:list") == "/ru/api/users/"
    assert resolve("/ru/api/users/").view_name == "users:list"


def test_user_me():
    assert reverse("users:me") == "/ru/api/users/me/"
    assert resolve("/ru/api/users/me/").view_name == "users:me"
