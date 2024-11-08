# tenentapp/forms.py

from django import forms
from .models import TenentProfile

class TenentProfileForm(forms.ModelForm):
    class Meta:
        model = TenentProfile
        fields = ['profile_image', 'phone_number', 'address']
