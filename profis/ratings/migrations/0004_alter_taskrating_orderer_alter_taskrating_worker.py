# Generated by Django 4.2.4 on 2023-12-27 12:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("ratings", "0003_remove_taskrating_adequacy_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="taskrating",
            name="orderer",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ratings_given",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Заказчик",
            ),
        ),
        migrations.AlterField(
            model_name="taskrating",
            name="worker",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ratings_received",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Исполнитель",
            ),
        ),
    ]
