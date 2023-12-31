# Generated by Django 4.2.4 on 2023-09-20 11:37

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Созданное время")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновленное время")),
                ("name", models.CharField(max_length=255, verbose_name="Категория")),
                ("slug", models.SlugField(max_length=255, unique=True)),
                (
                    "icon",
                    models.FileField(
                        upload_to="category",
                        validators=[django.core.validators.FileExtensionValidator(["svg", "png"])],
                        verbose_name="Иконка",
                    ),
                ),
                (
                    "parent_category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="child",
                        to="categories.category",
                        verbose_name="Родительская категория",
                    ),
                ),
            ],
            options={
                "verbose_name": "Категория",
                "verbose_name_plural": "Категории",
            },
        ),
    ]
