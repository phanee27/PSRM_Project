from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'image', 'overview', 'location', 'property_type',
                  'price', 'description', 'size', 'bedrooms', 'bathrooms',
                  'parking', 'year_built', 'flooring_type', 'owner_name',
                  'email', 'phone']


# forms.py

from django import forms
from .models import OwnerProfile


class OwnerProfileForm(forms.ModelForm):
    class Meta:
        model = OwnerProfile
        fields = ['profile_image', 'phone_number', 'address']


    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError("Phone number should only contain digits.")
        return phone_number
