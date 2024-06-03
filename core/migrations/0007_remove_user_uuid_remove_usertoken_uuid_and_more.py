# Generated by Django 5.0.6 on 2024-06-01 18:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0006_usertoken_sec_ua"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="uuid",
        ),
        migrations.RemoveField(
            model_name="usertoken",
            name="uuid",
        ),
        migrations.AlterField(
            model_name="user",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
        ),
        migrations.AlterField(
            model_name="user",
            name="id",
            field=models.AutoField(
                primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="更新时间"),
        ),
        migrations.AlterField(
            model_name="usertoken",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
        ),
        migrations.AlterField(
            model_name="usertoken",
            name="id",
            field=models.AutoField(
                primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="usertoken",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="更新时间"),
        ),
    ]