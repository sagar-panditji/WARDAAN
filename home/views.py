from django.shortcuts import render, HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
    login_required,
)
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from datetime import datetime, timedelta, date
from django.conf import settings
from django.db.models import Q
from .forms import LoginForm, DiseaseForm
from .models import Departments, Symptom, Disease, DSEnrollment
from doctor.models import Doctor
from patient.models import Patient
from hospital.models import Hospital


# Create your views here.


@login_required(login_url="login")
def home(request):
    departments = Departments.objects.all()
    d = {"departments": departments}
    return render(request, "home/home.html", d)


# @login_required(login_url="login")
def diseases(request):
    for d in Disease.objects.all():
        print(d.name)
        print(d.symptoms)
    d = {"d": d}
    return render(request, "home/diseases.html", d)


def add_disease(request):
    if request.method == "POST":
        form = DiseaseForm(request.POST)
        if form.is_valid():
            disease = Disease(name=form.cleaned_data["name"])
            disease.save()
            for qs in form.cleaned_data["symptoms"]:
                obj = DSEnrollment(disease=disease, symptom=qs).save()
            return HttpResponse("ok")
        else:
            return HttpResponse("dhang se kar error hai")
    else:
        form = DiseaseForm()
    d = {"form": form}
    return render(request, "home/add_disease.html", d)


@login_required(login_url="login")
def department(request, department=None):
    doctors = Doctor.objects.filter(department=department)
    hospitals = Hospital.objects.filter(department=department)
    if len(doctors) == 0 and len(hospitals) == 0:
        return HttpResponse(
            "Currently there is no doctor or hospital with this department"
        )
    d = {"doctors": doctors}
    return render(request, "home/department.html", d)


@login_required(login_url="login")
def department_list(request):
    departments = Departments.objects.all()
    d = {"departments": departments}
    return render(request, "home/list_department.html", d)


@login_required(login_url="login")
def doctor_home(request):
    doctors = Doctor.objects.all()
    d = {"doctors": doctors}
    return render(request, "doctor/dhome.html", d)


@login_required(login_url="login")
def doctor(request, pk):
    dactar = Doctor.objects.get(id=pk)
    d = {"doctor": dactar}
    return render(request, "doctor/particular_doctor.html", d)


@login_required(login_url="login")
def doctor_list(request):
    doctors = Doctor.objects.all()
    d = {"doctors": doctors}
    return render(request, "doctor/dlist.html", d)


@login_required(login_url="login")
def hospital_home(request):
    hospitals = Hospital.objects.all()
    d = {"hospitals": hospitals}
    return render(request, "hospital/hhome.html", d)


@login_required(login_url="login")
def hospital(request, pk):
    hospitul = Hospital.objects.get(id=pk)
    d = {"hospitals": hospitul}
    return render(request, "hospital/particular_hospital.html", d)


@login_required(login_url="login")
def hospital_list(request):
    hospitals = Hospital.objects.all()
    d = {"hospitals": hospitals}
    return render(request, "hospital/hlist.html", d)


@login_required(login_url="login")
def blogs(request):
    d = {}
    return HttpResponse("blogs")
    return render(request, "home/blog.html", d)


@login_required(login_url="login")
def exp(request):
    departments = Departments.objects.all()
    print("LEN-DEPTS", len(departments))
    d = {"departments": departments, "len": len(departments)}
    return render(request, "home/exp.html", d)


def login(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        form = LoginForm()
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                user = authenticate(username=username, password=password)
                if user:
                    auth_login(request, user)
                    messages.info(request, "You are logged in succesfully")
                    return redirect("home")
                else:
                    messages.error(request, "Invalid username or password")
            else:
                messages.error(request, "Invalid username or password")
        d = {"form": form}
        return render(request, "myauth/login.html", d)


@login_required(login_url="login")
def logout(request):
    auth_logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("home")
