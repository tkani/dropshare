from django.db import models
from login.models import *

class folder(models.Model):
    added_on = models.DateField()
    user_id = models.BigIntegerField()
    folder_original_name = models.CharField(max_length=255)
    folder_name = models.CharField(unique=True,max_length=100)
    folder_size = models.FloatField()
    folder_files = models.IntegerField()
    folder_users = models.IntegerField()
    folder_password = models.CharField(max_length=100)
    SECURE_CHOICES = [
    ('private', 'Private'),
    ('protected', 'Protected'),
    ]
    folder_secure = models.CharField(max_length=10, choices=SECURE_CHOICES)
    STATUS_CHOICES = [
    ('active', 'Active'),
    ('deactive', 'Deactive'),
    ]
    folder_status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    last_change=models.DateTimeField()

    def __str__(self):
        fields = [f"{field.name}={getattr(self, field.name)}" for field in self._meta.fields]
        return ', '.join(fields)

class shared_folder(models.Model):
    added_on = models.DateField()
    from_user_id = models.BigIntegerField()
    to_user_id = models.ForeignKey(users, on_delete=models.CASCADE)
    folder_id = models.BigIntegerField()
    folder_original_name = models.CharField(max_length=255)
    folder_name = models.CharField(max_length=255)
    folder_size = models.FloatField()
    folder_files = models.IntegerField()
    folder_password = models.CharField(max_length=100)
    STATUS_CHOICES = [
    ('active', 'Active'),
    ('deactive', 'Deactive'),
    ]
    folder_status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    last_change=models.DateTimeField()

    def __str__(self):
        fields = [f"{field.name}={getattr(self, field.name)}" for field in self._meta.fields]
        return ', '.join(fields)

class datahouse(models.Model):
    added_on = models.DateField()
    user_id = models.BigIntegerField()
    folder_id = models.BigIntegerField()
    file_original_name = models.CharField(max_length=255)
    file_name = models.ImageField(upload_to='datahouse/')
    file_size = models.FloatField()
    chunk_file_id = models.CharField(max_length=100)
    expiry_date = models.DateTimeField()
    file_password = models.CharField(max_length=100)
    SECURE_CHOICES = [
    ('public', 'Public'),
    ('private', 'Private'),
    ('protected', 'Protected'),
    ]
    file_secure = models.CharField(max_length=10, choices=SECURE_CHOICES)
    STATUS_CHOICES = [
    ('active', 'Active'),
    ('deactive', 'Deactive'),
    ]
    file_status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    last_change=models.DateTimeField()

    def __str__(self):
        fields = [f"{field.name}={getattr(self, field.name)}" for field in self._meta.fields]
        return ', '.join(fields)

class shared_datahouse(models.Model):
    added_on = models.DateField()
    from_user_id = models.BigIntegerField()
    to_user_id = models.ForeignKey(users, on_delete=models.CASCADE)
    folder_id = models.BigIntegerField()
    datahouse_id = models.BigIntegerField()
    file_original_name = models.CharField(max_length=255)
    file_name = models.ImageField(upload_to='datahouse/')
    file_size = models.FloatField()
    expiry_date = models.DateTimeField()
    file_password = models.CharField(max_length=100)
    SECURE_CHOICES = [
    ('public', 'Public'),
    ('private', 'Private'),
    ('protected', 'Protected'),
    ]
    file_secure = models.CharField(max_length=10, choices=SECURE_CHOICES)
    STATUS_CHOICES = [
    ('active', 'Active'),
    ('deactive', 'Deactive'),
    ]
    file_status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    last_change=models.DateTimeField()

    def __str__(self):
        fields = [f"{field.name}={getattr(self, field.name)}" for field in self._meta.fields]
        return ', '.join(fields)


class setting(models.Model):
    added_on = models.DateField()
    user_id = models.BigIntegerField(unique=True)
    storage = models.FloatField()
    current_storage = models.FloatField()
    plan_id = models.BigIntegerField()
    plan_name = models.CharField(max_length=255)
    plan_expiray_date = models.DateTimeField()
    STATUS_CHOICES = [
    ('active', 'Active'),
    ('deactive', 'Deactive'),
    ]
    file_status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    last_change=models.DateTimeField()

    def __str__(self):
        fields = [f"{field.name}={getattr(self, field.name)}" for field in self._meta.fields]
        return ', '.join(fields)