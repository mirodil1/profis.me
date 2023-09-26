import pytest

from profis.categories.models import Category
from profis.categories.tests.factories import CategoryFactory
from profis.users.models import User
from profis.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user(db) -> User:
    return UserFactory()


@pytest.fixture
def category(db) -> Category:
    return CategoryFactory()
