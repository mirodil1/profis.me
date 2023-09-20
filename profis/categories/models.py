from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from profis.core.models import TimeStampedModel


class Category(TimeStampedModel):
    """
    Category model
    """

    name = models.CharField(max_length=255, verbose_name=_("Категория"))
    slug = models.SlugField(max_length=255, unique=True)
    icon = models.FileField(
        upload_to="category",
        null=True,
        blank=True,
        validators=[FileExtensionValidator(["svg", "png"])],
        verbose_name=_("Иконка"),
    )
    parent_category = models.ForeignKey(
        "self",
        related_name="child",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_("Родительская категория"),
    )

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
