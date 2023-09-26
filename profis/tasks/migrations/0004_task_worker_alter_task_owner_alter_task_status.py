# Generated by Django 4.2.4 on 2023-09-25 12:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("tasks", "0003_task_budget_taskresponse_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="worker",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="worker_task",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Исполнитель",
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="owner_task",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="status",
            field=models.CharField(
                choices=[
                    ("open", "Открыто"),
                    ("in_progress", "Выполняется"),
                    ("completed", "Выполнено"),
                    ("not_completed", "Не выполнено"),
                    ("closed", "Закрыто"),
                ],
                default="closed",
                max_length=15,
            ),
        ),
    ]
