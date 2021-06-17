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


class SearchHospitalForm(forms.Form):
    city = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter your city",
                "class": "form-control",
                "aria-label": "First name",
            }
        ),
    )
    hospital = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter Hospital",
                "class": "form-control",
                "aria-label": "First name",
            }
        ),
    )
