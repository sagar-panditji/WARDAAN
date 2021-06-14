from django.shortcuts import render, HttpResponse
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Doctor
from .forms import DoctorSignUpForm, SearchDoctorForm
from home.forms import UserSignUpForm
from django.contrib.auth.models import User
from home.models import Departments
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from home.views import (
    give_doctors_of_this_department,
    give_hospitals_of_this_department,
)


def best_card(request):
    return render(request, "doctor/best_card.html")


def doc_exp(request):
    doctors = Doctor.objects.all()
    d = {"doctors": doctors}
    return render(request, "doctor/exp.html", d)


def doc_home(request):
    doctors = Doctor.objects.all()
    print("DDDDD", doctors[0].user.username)
    departments = Departments.objects.all()
    form = SearchDoctorForm()
    if request.method == "POST":
        form = SearchDoctorForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data["city"]
            doctor_name = form.cleaned_data["doctor"]
            if city_name and doctor_name:
                filter_doctors = Doctor.objects.filter(city=city_name).filter(
                    user__username=doctor_name
                )
                if filter_doctors:
                    return HttpResponse(filter_doctors)
                else:
                    return HttpResponse("No Doctor Found")
            if city_name:
                filter_doctors = Doctor.objects.filter(city=city_name)
                if filter_doctors:
                    return HttpResponse(filter_doctors)
                else:
                    return HttpResponse("No doctor found")
            if doctor_name:
                filter_doctor = Doctor.objects.filter(user__username=doctor_name)
                if filter_doctor:
                    return HttpResponse(filter_doctor)
                else:
                    return HttpResponse("No doctor found")
    d = {
        "doctors": doctors,
        "departments": departments,
        "user": request.user,
        "form": form,
    }
    return render(request, "doctor/dhome.html", d)


def doc_profile(request, pk):
    dactar = Doctor.objects.get(id=pk)
    d = {"doctor": dactar}
    return render(request, "doctor/doc_profile.html", d)


def doc_list(request):
    doctors = Doctor.objects.all()
    d = {"doctors": doctors}
    return render(request, "doctor/dlist.html", d)


def dcard(request):
    d = {"obj": "obj"}
    return render(request, "home/dcard.html", d)


def doc_signup(request):
    if request.method == "POST":
        uform = UserSignUpForm(request.POST)
        dform = DoctorSignUpForm(request.POST)
        if not uform.is_valid():
            print("UUU FORM", uform)
            print()
            print()
        if not dform.is_valid():
            print("DDD FORM", dform)
            print()
            print()
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
            for dgr in dform.cleaned_data["degree"]:
                doctor.degree.add(dgr)
            doctor.save()
            return HttpResponse("ok")
        else:
            return HttpResponse("unmatched password or invalid form")
    else:
        uform = UserSignUpForm()
        dform = DoctorSignUpForm()
    context = {"uform": uform, "dform": dform}
    return render(request, "doctor/signup.html", context)
