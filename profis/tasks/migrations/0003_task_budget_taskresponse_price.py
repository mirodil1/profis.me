# Generated by Django 4.2.4 on 2023-09-25 06:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0002_taskresponse"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="budget",
            field=models.PositiveIntegerField(default=0, verbose_name="Бюджет"),
        ),
        migrations.AddField(
            model_name="taskresponse",
            name="price",
            field=models.PositiveIntegerField(default=0, verbose_name="Цена"),
        ),
    ]
