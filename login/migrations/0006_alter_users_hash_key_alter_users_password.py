# Generated by Django 5.0.1 on 2024-01-07 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("login", "0005_alter_users_hash_key_alter_users_password"),
    ]

    operations = [
        migrations.AlterField(
            model_name="users",
            name="hash_key",
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name="users",
            name="password",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]