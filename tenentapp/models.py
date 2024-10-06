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