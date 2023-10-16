from django.core.validators import FileExtensionValidator
from django.db import models
from django.template import defaultfilters
from django.utils.translation import gettext_lazy as _
from unidecode import unidecode

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
    price = models.DecimalField(default=0, max_digits=9, decimal_places=2, verbose_name=_("Цена"))
    order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )

    class Meta:
        ordering = ["order"]
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")

    def save(self, *args, **kwargs):
        self.slug = defaultfilters.slugify(unidecode(self.name))
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
