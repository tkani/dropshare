# Generated by Django 5.0.1 on 2024-01-09 03:48

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="shared_datahouse",
            name="datahouse_id",
            field=models.BigIntegerField(default=None),
            preserve_default=False,
        ),
    ]