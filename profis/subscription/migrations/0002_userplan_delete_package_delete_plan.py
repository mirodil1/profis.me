# Generated by Django 4.2.4 on 2023-10-19 07:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("categories", "0005_category_base_price_100_category_base_price_25_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("subscription", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserPlan",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Созданное время"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Обновленное время"
                    ),
                ),
                ("expired_at", models.DateTimeField(verbose_name="Срок действия")),
                (
                    "plan_type",
                    models.CharField(
                        choices=[("unlim", "Безлимитный"), ("base", "Базовый")],
                        verbose_name="Тип тарифа",
                    ),
                ),
                (
                    "categories",
                    models.ManyToManyField(
                        to="categories.category", verbose_name="Категории"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользовател",
                    ),
                ),
            ],
            options={
                "verbose_name": "План пользователей",
                "verbose_name_plural": "Планы пользователей",
            },
        ),
        migrations.DeleteModel(
            name="Package",
        ),
        migrations.DeleteModel(
            name="Plan",
        ),
    ]
