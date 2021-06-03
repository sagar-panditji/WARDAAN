from django import forms
from django.forms.utils import ValidationError
from .models import Patient
from django.contrib.auth.models import User


class PatientSignUpForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            "role",
            "date_of_birth",
            "gender",
            "mobile",
            "address",
            "city",
            "state",
            # "profile_pic",
        ]
