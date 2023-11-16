from django.urls import resolve, reverse


def test_category_list():
    assert reverse("categories:list") == "/ru/api/categories/"
    assert resolve("/ru/api/categories/").view_name == "categories:list"
