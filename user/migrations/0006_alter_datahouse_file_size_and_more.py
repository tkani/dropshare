# Generated by Django 5.0.1 on 2024-01-11 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0005_alter_setting_current_storage_alter_setting_storage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="datahouse", name="file_size", field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="shared_datahouse", name="file_size", field=models.FloatField(),
        ),
    ]
