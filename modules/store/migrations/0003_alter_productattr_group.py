# Generated by Django 5.0.6 on 2024-06-12 06:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0002_productattr_group_productskuvaluerelation_image_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productattr",
            name="group",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="store.productattrgroup",
            ),
        ),
    ]
