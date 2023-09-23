# Generated by Django 4.2.4 on 2023-09-23 09:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("categories", "0002_alter_category_icon"),
        ("users", "0004_alter_user_options_alter_user_is_worker"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="categories",
            field=models.ManyToManyField(
                blank=True, null=True, related_name="user_category", to="categories.category", verbose_name="Категории"
            ),
        ),
    ]
