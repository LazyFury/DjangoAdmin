# Generated by Django 5.0.6 on 2024-05-30 09:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_user_uuid_usertoken_uuid"),
    ]

    operations = [
        migrations.AddField(
            model_name="usertoken",
            name="expire_at",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name="usertoken",
            name="token",
            field=models.CharField(default=1, max_length=320, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="usertoken",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
