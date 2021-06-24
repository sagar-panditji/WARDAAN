from django import forms
from django.forms.utils import ValidationError
from .models import Doctor
from django.contrib.auth.models import User


class DoctorSignUpForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = [
            "department",
            "hospital",
            "clinic",
            "degree",
            "open_time",
            "close_time",
            "fees",
            "gender",
            "mobile",
            "address",
            "city",
            "state",
            "date_of_birth",
            # "profile_pic",
        ]


class SearchDoctorForm(forms.Form):
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
    doctor = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter Doctor",
                "class": "form-control",
                "aria-label": "First name",
            }
        ),
    )


class CompareDoctor(forms.Form):
    doctor1 = forms.ModelMultipleChoiceField(queryset=Doctor.objects.all())
    doctor2 = forms.ModelMultipleChoiceField(queryset=Doctor.objects.all())
