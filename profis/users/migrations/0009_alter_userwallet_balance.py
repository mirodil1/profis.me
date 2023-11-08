# Generated by Django 4.2.4 on 2023-10-23 07:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0008_alter_user_categories"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userwallet",
            name="balance",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=10, verbose_name="Баланс"
            ),
        ),
    ]
