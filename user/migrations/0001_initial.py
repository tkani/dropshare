# Generated by Django 5.0.1 on 2024-01-09 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="datahouse",
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
                ("folder_id", models.BigIntegerField()),
                ("file_original_name", models.CharField(max_length=255)),
                ("file_name", models.ImageField(upload_to="datahouse/")),
                ("file_size", models.IntegerField()),
                ("expiry_date", models.DateTimeField()),
                ("file_password", models.CharField(max_length=100, unique=True)),
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
            name="setting",
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
                ("storage", models.IntegerField()),
                ("current_storage", models.IntegerField()),
                ("plan_id", models.BigIntegerField()),
                ("plan_name", models.CharField(max_length=255)),
                ("plan_expiray_date", models.DateTimeField()),
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
            name="shared_datahouse",
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
                ("to_user_id", models.BigIntegerField()),
                ("folder_id", models.BigIntegerField()),
                ("file_original_name", models.CharField(max_length=255)),
                ("file_name", models.ImageField(upload_to="datahouse/")),
                ("file_size", models.IntegerField()),
                ("expiry_date", models.DateTimeField()),
                ("file_password", models.CharField(max_length=100, unique=True)),
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
    ]