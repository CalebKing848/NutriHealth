from typing import Self
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserInformation
from .models import ContactInformation

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