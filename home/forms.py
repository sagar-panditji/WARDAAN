from django import forms
from django.contrib.auth.models import User
from .models import *


class BookAppointmentForm(forms.ModelForm):
    class Meta:
        model = BookAppointment
        fields = ["symptoms", "description"]


class DiseaseForm(forms.ModelForm):
    class Meta:
        model = Disease
        fields = ["name", "symptoms"]


class SymptomForm(forms.ModelForm):
    class Meta:
        model = Symptom
        fields = ["name"]


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Username"})
    )
    password = forms.CharField(
        # widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )


class UserSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "password",
            "confirm_password",
            "email",
        ]
