# Generated by Django 5.0.1 on 2024-01-14 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0008_alter_datahouse_file_secure"),
    ]

    operations = [
        migrations.AlterField(
            model_name="setting",
            name="user_id",
            field=models.BigIntegerField(unique=True),
        ),
    ]
