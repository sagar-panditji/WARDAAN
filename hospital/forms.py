from django import forms
from django.forms.utils import ValidationError
from .models import Hospital
from django.contrib.auth.models import User


class HospitalSignUpForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = [
            "department",
            "mobile",
            "address",
            "city",
            "state",
            # "profile_pic",
        ]
