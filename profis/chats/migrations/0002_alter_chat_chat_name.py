# Generated by Django 4.2.4 on 2023-12-13 10:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chats", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chat",
            name="chat_name",
            field=models.CharField(max_length=64, unique=True, verbose_name="ads"),
        ),
    ]
