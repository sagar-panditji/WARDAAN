from django import forms
from django.forms.utils import ValidationError
from .models import Doctor
from django.contrib.auth.models import User


class DoctorSignUpForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = [
            "department",
            "clinic",
            "degree",
            "clinic_open_time",
            "clinic_close_time",
            "fees",
            "gender",
            "mobile",
            "address",
            "city",
            "state",
            "date_of_birth",
            # "profile_pic",
        ]
