from django.shortcuts import render, HttpResponse
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Patient
from .forms import PatientSignUpForm
from doctor.models import BookAppointment, Review, Doctor
from blogs.models import Blogs
from home.forms import UserSignUpForm
from home.views import (
    extract_all_doctors_for_patient_from_appointments,
    give_approved_appointments,
)
from django.contrib.auth.models import User
import os
from django.core.files.storage import FileSystemStorage


def signup(request):
    if request.method == "POST":
        uform = UserSignUpForm(request.POST)
        pform = PatientSignUpForm(request.POST)
        if uform.is_valid() and pform.is_valid():
            ### Creating User ###
            user = uform.save()
            user.first_name = uform.cleaned_data["first_name"]
            user.last_name = uform.cleaned_data["last_name"]
            user.username = uform.cleaned_data["username"]
            user.email = uform.cleaned_data["email"]
            user.password = uform.cleaned_data["password"]
            user.confirm_password = uform.cleaned_data["confirm_password"]
            user.set_password(user.password)
            user.save()
            ### Creating Patient ###
            patient = pform.save(commit=False)
            patient.user = user
            patient.gender = pform.cleaned_data["gender"]
            patient.mobile = pform.cleaned_data["mobile"]
            patient.address = pform.cleaned_data["address"]
            patient.city = pform.cleaned_data["city"]
            patient.state = pform.cleaned_data["state"]
            patient.date_of_birth = pform.cleaned_data["date_of_birth"]
            patient.save()
            return render("home")
        else:
            return HttpResponse("unmatched password or invalid form")
    else:
        uform = UserSignUpForm()
        pform = PatientSignUpForm()
    context = {"uform": uform, "pform": pform}
    return render(request, "patient/signup.html", context)


def pat_profile(request, pk):
    print("HELLOO PATTT")
    user = request.user
    patient = Patient.objects.get(id=pk)
    records = BookAppointment.objects.filter(patient_id=pk)
    records = records[::-1]
    blogs = Blogs.objects.all().filter(user=patient.user)[::-1]
    try:
        ispatient = user.patient.id
    except:
        ispatient = 0
    ### fetching review doctor form
    try:
        rating = request.GET["rating"]
        rating, record_id = rating.split("=")
        description = request.GET["description"]
    except:
        rating = description = None
    try:
        record = BookAppointment.objects.get(id=record_id)
        doctor = Doctor.objects.get(id=record.doctor_id)
        doctor.cnt += 1
        doctor.rating += int(rating)
        doctor.save()
    except:
        record = None
    if rating or description:
        print("YOYO", rating, description)
        obj = Review.objects.create()
        obj.rating = int(rating)
        obj.description = description
        obj.patient_id = patient.id
        obj.doctor_id = record.doctor_id
        obj.save()
    # yha medical history logic
    dactars = extract_all_doctors_for_patient_from_appointments(patient)
    try:
        appointments = give_approved_appointments(pk)
    except:
        appointments = []
    try:
        iddd = request.GET["doctor"]
        doc = Doctor.objects.get(id=int(iddd))
        documents = []
        ln = len(documents)
    except:
        doc = None
        documents = []
        ln = len(documents)
    d = {
        "patient": patient,
        "records": records,
        "ispatient": ispatient,
        "blogs": blogs,
        "doctors": dactars,
        "documents": documents,
        "doc": doc,
        "ln": 0,
        "appointments": appointments,
    }
    return render(request, "patient/pat_profile.html", d)


def particular_appointment(request, pk):
    url = None
    print("HELL PARTICULARRRRR")
    user = request.user
    usertype = {"doc": 0, "pat": 0}
    if request.user.is_authenticated:
        try:
            if user.doctor:
                usertype["doc"] = 1
        except:
            usertype["pat"] = 1
    try:
        try:
            document = request.FILES["file"]
        except:
            print("document nahi mila")
        print("try chala of ducment", document)
        obj = BookAppointment.objects.get(id=pk)
        obj.document = document
        obj.save()
        print("DOCUMENTTTT", document)
    except:
        document = None
        print("exept chala of document")
    record = BookAppointment.objects.get(id=pk)
    doctor = Doctor.objects.get(id=record.doctor_id)
    patient = Patient.objects.get(id=record.patient_id)
    d = {
        "record": record,
        "doctor": doctor,
        "patient": patient,
        "usertype": usertype,
        "url": url,
    }
    return render(request, "patient/particular_appointment.html", d)


def submit_fees(request, pk):
    record = BookAppointment.objects.get(id=pk)
    patient = Patient.objects.get(id=record.patient_id)
    doctor = Doctor.objects.get(id=record.doctor_id)
    record.fees_submitted = 1
    record.save()
    return HttpResponse("submit fees")
