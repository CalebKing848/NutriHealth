from typing import Self
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserInformation
from .models import ContactInformation
from .models import FoodItem
from .models import DailyIntakeItem


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserInformationForm(forms.ModelForm):
    class Meta:
        model = UserInformation
        fields = ["age", "gender", "weight", "height", "energy_intake", "existing_medical_conditions"]

class ContactInformationForm(forms.ModelForm):
    class Meta:
        model = ContactInformation
        fields = ["name", "email", "message"]


class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['code', 'name', 'serving_size', 'energy', 'protein', 'fat', 'carbohydrates']

class DailyIntakeItemForm(forms.ModelForm):
    class Meta:
        model = DailyIntakeItem
        fields = ['food_item', 'quantity']
        widgets = {
            'food_item': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }