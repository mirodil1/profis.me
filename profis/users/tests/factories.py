from collections.abc import Sequence
from typing import Any

from django.contrib.auth import get_user_model
from factory import Faker, post_generation
from factory.django import DjangoModelFactory, ImageField

from profis.users.models import UserWallet


class WalletFactory(DjangoModelFactory):
    class Meta:
        model = UserWallet


class UserFactory(DjangoModelFactory):
    email = Faker("email")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    bio = Faker("sentence")
    work_experiance = Faker("random_int", min=1, max=12)
    gender = Faker("bool")
    avatar = ImageField()
    gender = Faker("random_element", elements=["m", "f"])
    is_worker = Faker("boolean")
    number_of_views = Faker("random_int", min=0, max=1000000)

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).evaluate(None, None, extra={"locale": None})
        )
        self.set_password(password)

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        """Save again the instance if creating and at least one hook ran."""
        if create and results and not cls._meta.skip_postgeneration_save:
            # Some post-generation hooks ran, and may have modified us.
            instance.save()

    class Meta:
        model = get_user_model()
        django_get_or_create = ["email"]
