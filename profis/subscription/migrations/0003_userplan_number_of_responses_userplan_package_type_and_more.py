# Generated by Django 4.2.4 on 2023-10-20 13:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("categories", "0005_category_base_price_100_category_base_price_25_and_more"),
        ("subscription", "0002_userplan_delete_package_delete_plan"),
    ]

    operations = [
        migrations.AddField(
            model_name="userplan",
            name="number_of_responses",
            field=models.PositiveSmallIntegerField(
                blank=True, null=True, verbose_name="Количество откликов"
            ),
        ),
        migrations.AddField(
            model_name="userplan",
            name="package_type",
            field=models.CharField(
                choices=[
                    ("unlim_15", "Безлимитный 15"),
                    ("unlim_30", "Безлимитный 30"),
                    ("unlim_90", "Безлимитный 90"),
                    ("base_25", "Базовый 25"),
                    ("base_50", "Базовый 50"),
                    ("base_100", "Базовый 100"),
                ],
                default=1,
                verbose_name="Тип пакета",
            ),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name="userplan",
            name="categories",
        ),
        migrations.AddField(
            model_name="userplan",
            name="categories",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="categories.category",
                verbose_name="Категории",
            ),
            preserve_default=False,
        ),
    ]