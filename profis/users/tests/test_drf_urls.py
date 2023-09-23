from django.urls import resolve, reverse

from profis.users.models import User


def test_user_detail(user: User):
    assert reverse("users:detail", kwargs={"id": user.id}) == f"/api/users/{user.id}/"
    assert resolve(f"/api/users/{user.pk}/").view_name == "users:detail"


def test_user_list():
    assert reverse("users:list") == "/api/users/"
    assert resolve("/api/users/").view_name == "users:list"


def test_user_me():
    assert reverse("users:me") == "/api/users/me/"
    assert resolve("/api/users/me/").view_name == "users:me"
