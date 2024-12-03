from django import forms
from .models import Property, RentalContract


from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'image', 'image_2', 'image_3', 'overview', 'location', 'location_url', 'address',
            'property_type', 'price', 'description', 'size', 'bedrooms', 'bathrooms',
            'parking', 'year_built', 'flooring_type', 'owner_name', 'email', 'phone', 'occupancy_status'
        ]


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


class RentalContractForm(forms.ModelForm):
    class Meta:
        model = RentalContract
        fields = ['property', 'tenant', 'agreement_file', 'status', 'start_date', 'end_date']


from django import forms


class ContractForm(forms.Form):
    AGREEMENT_TYPE_CHOICES = [
        ('rental', 'Rental Agreement'),
        ('sale', 'Sale Agreement'),
    ]

    agreement_type = forms.ChoiceField(choices=AGREEMENT_TYPE_CHOICES, label='Agreement Type')

    # Common fields for both agreements
    tenant_name = forms.CharField(label='Tenant/Buyer Name', max_length=100)
    tenant_email = forms.EmailField(label='Tenant/Buyer Email')
    tenant_address = forms.CharField(label='Tenant/Buyer Address', widget=forms.Textarea)
    owner_name = forms.CharField(label='Owner/Seller Name', max_length=100)
    owner_email = forms.EmailField(label='Owner/Seller Email')
    owner_address = forms.CharField(label='Owner/Seller Address', widget=forms.Textarea)
    property_address = forms.CharField(label='Property Address', widget=forms.Textarea)

    # Rental-specific fields
    rental_amount = forms.DecimalField(label='Rental Amount', max_digits=10, decimal_places=2, required=False)
    start_date = forms.DateField(label='Lease Start Date', widget=forms.SelectDateWidget, required=False)
    end_date = forms.DateField(label='Lease End Date', widget=forms.SelectDateWidget, required=False)
    security_deposit = forms.DecimalField(label='Security Deposit', max_digits=10, decimal_places=2, required=False)

    # Sale-specific fields
    sale_price = forms.DecimalField(label='Sale Price', max_digits=10, decimal_places=2, required=False)
    sale_date = forms.DateField(label='Sale Date', widget=forms.SelectDateWidget, required=False)

from django import forms
from ownerapp.models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your message here...',
                'rows': 4,
            }),
        }


from django import forms
from .models import Reply

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Type your reply...'}),
        }

