from django.shortcuts import render, HttpResponse
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime, timedelta, date
from django.conf import settings
from django.db.models import Q
from .models import Departments, Symptoms, Disease
from doctor.models import Doctor
from patient.models import Patient
from hospital.models import Hospital

# Create your views here.
def home(request):
    departments = Departments.objects.all()
    d = {"departments": departments}
    return render(request, "home/home.html", d)


def department(request, department=None):
    doctors = Doctor.objects.filter(department=department)
    hospitals = Hospital.objects.filter(department=department)
    if len(doctors) == 0 and len(hospitals) == 0:
        return HttpResponse(
            "Currently there is no doctor or hospital with this department"
        )
    d = {"doctors": doctors}
    return render(request, "home/department.html", d)


def department_list(request):
    departments = Departments.objects.all()
    d = {"departments": departments}
    return render(request, "home/list_department.html", d)


def doctor_home(request):
    doctors = Doctor.objects.all()
    d = {"doctors": doctors}
    return render(request, "doctor/dhome.html", d)


def doctor(request, pk):
    dactar = Doctor.objects.get(id=pk)
    d = {"doctor": dactar}
    return render(request, "doctor/particular_doctor.html", d)


def doctor_list(request):
    doctors = Doctor.objects.all()
    d = {"doctors": doctors}
    return render(request, "doctor/dlist.html", d)


def hospital_home(request):
    hospitals = Hospital.objects.all()
    d = {"hospitals": hospitals}
    return render(request, "hospital/hhome.html", d)


def hospital(request, pk):
    hospitul = Hospital.objects.get(id=pk)
    d = {"hospitals": hospitul}
    return render(request, "hospital/particular_hospital.html", d)


def hospital_list(request):
    hospitals = Hospital.objects.all()
    d = {"hospitals": hospitals}
    return render(request, "hospital/hlist.html", d)


def blogs(request):
    d = {}
    return HttpResponse("blogs")
    return render(request, "home/blog.html", d)


def exp(request):
    departments = Departments.objects.all()
    print("LEN-DEPTS", len(departments))
    d = {"departments": departments, "len": len(departments)}
    return render(request, "home/exp.html", d)
