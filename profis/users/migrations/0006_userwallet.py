# Generated by Django 4.2.4 on 2023-09-24 14:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0005_user_categories"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserWallet",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Созданное время")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновленное время")),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False, unique=True, verbose_name="ID"
                    ),
                ),
                ("balance", models.PositiveIntegerField(default=0, verbose_name="Баланс")),
                (
                    "status",
                    models.CharField(
                        choices=[("active", "Активный"), ("frozen", "Замароженный"), ("closed", "Закрытый")],
                        default="active",
                        max_length=6,
                        verbose_name="Статус",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
