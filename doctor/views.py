from django.shortcuts import render, HttpResponse
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Doctor
from .forms import DoctorSignUpForm
from home.forms import UserSignUpForm
from django.contrib.auth.models import User
from home.models import Departments


def signup(request):
    if request.method == "POST":
        uform = UserSignUpForm(request.POST)
        dform = DoctorSignUpForm(request.POST)
        if uform.is_valid() and dform.is_valid():
            ### Creating User ###
            user = uform.save()
            user.first_name = uform.cleaned_data["first_name"]
            user.last_name = uform.cleaned_data["last_name"]
            user.username = uform.cleaned_data["username"]
            user.email = uform.cleaned_data["email"]
            user.password = uform.cleaned_data["password"]
            user.save()
            ### Creating Doctor ###
            doctor = dform.save(commit=False)
            doctor.user = user
            doctor.department = dform.cleaned_data["department"]
            doctor.clinic = dform.cleaned_data["clinic"]
            doctor.gender = dform.cleaned_data["gender"]
            doctor.mobile = dform.cleaned_data["mobile"]
            doctor.address = dform.cleaned_data["address"]
            doctor.city = dform.cleaned_data["city"]
            doctor.state = dform.cleaned_data["state"]
            doctor.date_of_birth = dform.cleaned_data["date_of_birth"]
            doctor.save()
            return HttpResponse("ok")
        else:
            return HttpResponse("unmatched password or invalid form")
    else:
        uform = UserSignUpForm()
        dform = DoctorSignUpForm()
    context = {"uform": uform, "dform": dform}
    return render(request, "doctor/signup.html", context)
