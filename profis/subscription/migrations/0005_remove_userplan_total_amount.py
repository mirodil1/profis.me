# Generated by Django 4.2.4 on 2023-10-23 07:17

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("subscription", "0004_userplan_total_amount"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userplan",
            name="total_amount",
        ),
    ]
