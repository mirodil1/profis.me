# Generated by Django 4.2.4 on 2023-12-29 09:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("tasks", "0012_taskaddress_coords"),
    ]

    operations = [
        migrations.CreateModel(
            name="TaskResponseTemplate",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Созданное время")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновленное время")),
                ("title", models.CharField(max_length=128, verbose_name="")),
                ("description", models.TextField(verbose_name="")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="task_template",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]