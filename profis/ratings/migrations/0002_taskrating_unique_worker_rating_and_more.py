# Generated by Django 4.2.4 on 2023-10-05 14:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ratings", "0001_initial"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="taskrating",
            constraint=models.UniqueConstraint(fields=("worker", "task"), name="unique_worker_rating"),
        ),
        migrations.AddConstraint(
            model_name="taskrating",
            constraint=models.UniqueConstraint(fields=("orderer", "task"), name="unique_orderer_rating"),
        ),
    ]
