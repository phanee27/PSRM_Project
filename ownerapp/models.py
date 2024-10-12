from django.db import models
from django.contrib.auth.models import User

class OwnerUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150)  # Will match the username in User
    email = models.EmailField()
    password = models.CharField(max_length=128)  # For storing the hashed password

    def _str_(self):
        return f'{self.username} - {self.email}'


from django.db import models
from django.contrib.auth.models import User

class Property(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('Rent', 'Rent'),
        ('Sale', 'Sale'),
    ]

    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='property_images/')
    overview = models.TextField()
    location = models.CharField(max_length=200)
    property_type = models.CharField(max_length=10, choices=PROPERTY_TYPE_CHOICES, default='Rent')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    size = models.PositiveIntegerField()  # Property size in square feet
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    parking = models.CharField(max_length=20)  # Available / Not Available
    year_built = models.PositiveIntegerField()
    flooring_type = models.CharField(max_length=100)
    owner_name = models.CharField(max_length=100, default='Unknown Owner')  # You can also link this to the user model
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    occupancy_status = models.CharField(max_length=20, default='Available')  # Available or Rented
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties', default=1)

    def __str__(self):
        return self.title


# models.py

from django.db import models
from django.contrib.auth.models import User


class OwnerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
