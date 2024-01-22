from django.db import models

class users(models.Model):
    added_on = models.DateField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email_id = models.EmailField(unique=True, max_length=100)
    mobile_no = models.CharField(unique=True, max_length=20)
    password = models.CharField(unique=True,max_length=100)
    secret_key = models.CharField(max_length=255)
    hash_key = models.CharField(unique=True,max_length=100)
    old_file_name = models.CharField(max_length=255)
    profile = models.ImageField(upload_to='profile_images/')
    AGREEMENT_CHOICES = [
    ('agree', 'Agree'),
    ('disagree', 'Disagree'),
    ]
    agreement = models.CharField(max_length=10, choices=AGREEMENT_CHOICES)
    STATUS_CHOICES = [
    ('active', 'Active'),
    ('deactive', 'Deactive'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    last_change=models.DateTimeField()

    def __str__(self):
        fields = [f"{field.name}={getattr(self, field.name)}" for field in self._meta.fields]
        return ', '.join(fields)