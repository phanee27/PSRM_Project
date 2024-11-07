from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class TenentUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def _str_(self):
        return self.username


# tenentapp/models.py

from django.db import models
from django.contrib.auth.models import User


class TenentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='tenent_profile_images/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
