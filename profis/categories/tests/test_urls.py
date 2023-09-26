from django.urls import resolve, reverse


def test_category_list():
    assert reverse("categories:list") == "/api/categories/"
    assert resolve("/api/categories/").view_name == "categories:list"
