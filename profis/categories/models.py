from django.core.validators import FileExtensionValidator
from django.db import models
from django.template import defaultfilters
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
from unidecode import unidecode

from profis.core.models import TimeStampedModel


class Category(TimeStampedModel, TranslatableModel):
    """
    Category model
    """

    translations = TranslatedFields(
        name=models.CharField(max_length=255, db_index=True, verbose_name=_("Категория")),
        slug=models.SlugField(
            max_length=255,
            db_index=True,
        ),
        meta={"unique_together": [("slug", "language_code")]},
    )
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
    price = models.DecimalField(default=0, max_digits=9, decimal_places=2, verbose_name=_("Цена за 1 отклик"))
    post_price = models.DecimalField(default=0, max_digits=9, decimal_places=2, verbose_name=_("Цена после оплаты"))
    base_price_25 = models.DecimalField(
        default=0, max_digits=9, decimal_places=2, verbose_name=_("Цена пакета за 25 откликов")
    )
    base_price_50 = models.DecimalField(
        default=0, max_digits=9, decimal_places=2, verbose_name=_("Цена пакета за 25 откликов")
    )
    base_price_100 = models.DecimalField(
        default=0, max_digits=9, decimal_places=2, verbose_name=_("Цена пакета за 25 откликов")
    )
    unlim_price_15 = models.DecimalField(
        default=0, max_digits=9, decimal_places=2, verbose_name=_("Цена пакета на 15 дней")
    )
    unlim_price_30 = models.DecimalField(
        default=0, max_digits=9, decimal_places=2, verbose_name=_("Цена пакета на 30 дней")
    )
    unlim_price_90 = models.DecimalField(
        default=0, max_digits=9, decimal_places=2, verbose_name=_("Цена пакета на 90 дней")
    )

    order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")

    def get_level(self):
        level = 0
        current_category = self
        while current_category.parent_category is not None:
            level += 1
            current_category = current_category.parent_category
        return level

    def save(self, *args, **kwargs):
        self.slug = defaultfilters.slugify(unidecode(self.name))
        return super().save(*args, **kwargs)

    def __unicode__(self) -> str:
        return self.name
