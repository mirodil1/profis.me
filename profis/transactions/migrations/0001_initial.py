# Generated by Django 4.2.4 on 2023-12-13 10:47

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Transaction",
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
                (
                    "_id",
                    models.CharField(
                        db_index=True, max_length=255, verbose_name="ID Транзакции"
                    ),
                ),
                (
                    "user_id",
                    models.IntegerField(
                        db_index=True, null=True, verbose_name="ID Пользователя"
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Сумма"
                    ),
                ),
                (
                    "state",
                    models.IntegerField(
                        blank=True, default=1, null=True, verbose_name=""
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("processing", "В процессе"),
                            ("success", "Успешно"),
                            ("failed", "Ошибка"),
                            ("canceled", "Отменено"),
                        ],
                        max_length=55,
                        verbose_name="Статус транзакции",
                    ),
                ),
                ("create_time", models.BigIntegerField(null=True)),
                ("perform_time", models.BigIntegerField(null=True)),
                ("cancel_time", models.BigIntegerField(null=True)),
                ("reason", models.IntegerField(null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]