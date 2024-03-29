# Generated by Django 5.0.1 on 2024-01-09 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0003_alter_datahouse_file_password_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="datahouse",
            name="file_secure",
            field=models.CharField(
                choices=[("yes", "Yes"), ("no", "No")], default=None, max_length=10
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="shared_datahouse",
            name="file_secure",
            field=models.CharField(
                choices=[("yes", "Yes"), ("no", "No")], default=None, max_length=10
            ),
            preserve_default=False,
        ),
    ]
