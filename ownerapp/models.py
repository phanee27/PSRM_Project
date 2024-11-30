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
    image_2 = models.ImageField(upload_to='property_images/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='property_images/', blank=True, null=True)
    overview = models.TextField(max_length=100)
    location = models.CharField(max_length=200)
    address = models.TextField(max_length=300, blank=True, null=True)  # New address field
    property_type = models.CharField(max_length=10, choices=PROPERTY_TYPE_CHOICES, default='Rent')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    size = models.PositiveIntegerField()  # Property size in square feet
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    parking = models.CharField(max_length=20)  # Available / Not Available
    year_built = models.PositiveIntegerField()
    flooring_type = models.CharField(max_length=100)
    owner_name = models.CharField(max_length=100, default='Unknown Owner')
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    occupancy_status = models.CharField(max_length=20, default='Available')
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


from tenentapp.models import TenentUser

class RentalContract(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    tenant = models.ForeignKey(TenentUser, on_delete=models.CASCADE)
    agreement_file = models.FileField(upload_to='contracts/')
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Active', 'Active'), ('Completed', 'Completed')])
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey('Property', on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.tenant} to {self.owner} for {self.property.title}"


class Reply(models.Model):
    message = models.ForeignKey(Message, related_name='replies', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Owner replying
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='tenant_replies')  # Tenant replying
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply from {'Owner' if self.owner else 'Tenant'} to {self.message.tenant.username if self.tenant else self.message.owner.username}"


