from django import forms
from django.forms.utils import ValidationError
from .models import Doctor
from django.contrib.auth.models import User


class DoctorSignUpForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = [
            "role",
            "department",
            "clinic",
            "hospital",
            "date_of_birth",
            "gender",
            "mobile",
            "address",
            "city",
            "state",
            # "profile_pic",
        ]
