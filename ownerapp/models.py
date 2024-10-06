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

class Property(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('Rent', 'Rent'),
        ('Sale', 'Sale'),
    ]

    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='property_images/')
    overview = models.TextField()
    location = models.CharField(max_length=200)
    property_type = models.CharField(max_length=10, choices=PROPERTY_TYPE_CHOICES, default='Rent')  # Set a default value here
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    size = models.PositiveIntegerField()  # in sq. ft.
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    parking = models.CharField(max_length=20)  # Available / Not Available
    year_built = models.PositiveIntegerField()
    flooring_type = models.CharField(max_length=100)
    owner_name = models.CharField(max_length=100, default='Unknown Owner')
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.title
