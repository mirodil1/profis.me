# Generated by Django 4.2.4 on 2023-09-20 13:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("categories", "0002_alter_category_icon"),
    ]

    operations = [
        migrations.CreateModel(
            name="Task",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Созданное время")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновленное время")),
                ("name", models.CharField(max_length=255, verbose_name="Название задание")),
                ("description", models.TextField(verbose_name="Подробное описание")),
                ("phone_number", models.CharField(max_length=15, verbose_name="Номер телефона")),
                (
                    "status",
                    models.CharField(
                        choices=[("open", "Открыто"), ("closed", "Закрыто")], default="closed", max_length=15
                    ),
                ),
                ("start_time", models.DateTimeField(blank=True, null=True, verbose_name="Время начала")),
                ("finish_time", models.DateTimeField(blank=True, null=True, verbose_name="Время окончания")),
                ("file", models.FileField(blank=True, null=True, upload_to="", verbose_name="Файл")),
                ("number_of_views", models.PositiveIntegerField(default=0, verbose_name="Просмотры")),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="categories.category", verbose_name="Категория"
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Задание",
                "verbose_name_plural": "Задания",
            },
        ),
        migrations.CreateModel(
            name="TaskImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Созданное время")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновленное время")),
                ("image", models.ImageField(upload_to="tasks", verbose_name="Фото")),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="tasks.task",
                        verbose_name="Задание",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
