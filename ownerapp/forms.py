from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'image', 'overview', 'location', 'property_type',
                  'price', 'description', 'size', 'bedrooms', 'bathrooms',
                  'parking', 'year_built', 'flooring_type', 'owner_name',
                  'email', 'phone']
