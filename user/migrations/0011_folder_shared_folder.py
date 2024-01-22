# Generated by Django 5.0.1 on 2024-01-15 01:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("login", "0007_users_old_file_name"),
        ("user", "0010_alter_shared_datahouse_to_user_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="folder",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("added_on", models.DateField()),
                ("user_id", models.BigIntegerField()),
                ("folder_original_name", models.CharField(max_length=255)),
                ("folder_name", models.CharField(max_length=255)),
                ("folder_size", models.FloatField()),
                ("folder_files", models.IntegerField()),
                ("folder_users", models.IntegerField()),
                ("folder_password", models.CharField(max_length=100)),
                (
                    "folder_secure",
                    models.CharField(
                        choices=[("private", "Private"), ("protected", "Protected")],
                        max_length=10,
                    ),
                ),
                (
                    "file_status",
                    models.CharField(
                        choices=[("active", "Active"), ("deactive", "Deactive")],
                        max_length=10,
                    ),
                ),
                ("last_change", models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name="shared_folder",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("added_on", models.DateField()),
                ("from_user_id", models.BigIntegerField()),
                ("folder_id", models.BigIntegerField()),
                ("folder_original_name", models.CharField(max_length=255)),
                ("folder_name", models.CharField(max_length=255)),
                ("folder_password", models.CharField(max_length=100)),
                (
                    "file_status",
                    models.CharField(
                        choices=[("active", "Active"), ("deactive", "Deactive")],
                        max_length=10,
                    ),
                ),
                ("last_change", models.DateTimeField()),
                (
                    "to_user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="login.users"
                    ),
                ),
            ],
        ),
    ]
