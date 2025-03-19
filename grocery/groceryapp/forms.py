from django import forms
from .models import Product
from django import forms
from .models import Address

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "image", "description"] 
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter product name"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter price"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter product description", "rows": 3}),  # ✅ Added description input
        }


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["full_name", "phone_number", "street_address", "city", "state", "postal_code", "country"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Full Name"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone Number"}),
            "street_address": forms.Textarea(attrs={"class": "form-control", "placeholder": "Street Address", "rows": 2}),
            "city": forms.TextInput(attrs={"class": "form-control", "placeholder": "City"}),
            "state": forms.TextInput(attrs={"class": "form-control", "placeholder": "State"}),
            "postal_code": forms.TextInput(attrs={"class": "form-control", "placeholder": "Postal Code"}),
            "country": forms.TextInput(attrs={"class": "form-control", "placeholder": "Country"}),
        }

