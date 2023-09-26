from factory import Faker
from factory.django import DjangoModelFactory

from profis.categories.models import Category


class CategoryFactory(DjangoModelFactory):
    name = Faker("word")
    slug = name

    class Meta:
        model = Category
