from django import forms
from django.forms.utils import ValidationError
from .models import Hospital
from django.contrib.auth.models import User


class HospitalSignUpForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = [
            "departments",
            "no_of_beds",
            "mobile",
            "address",
            "city",
            "state",
            # "profile_pic",
        ]
