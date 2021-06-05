from django import forms
from django.forms.utils import ValidationError
from .models import Patient
from django.contrib.auth.models import User


class PatientSignUpForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            "gender",
            "mobile",
            "address",
            "city",
            "state",
            "date_of_birth",
            # "profile_pic",
        ]
