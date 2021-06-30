from django.shortcuts import render, HttpResponse
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Patient
from .forms import PatientSignUpForm
from doctor.models import BookAppointment, Review
from home.forms import UserSignUpForm
from django.contrib.auth.models import User


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
            return HttpResponse("ok")
        else:
            return HttpResponse("unmatched password or invalid form")
    else:
        uform = UserSignUpForm()
        pform = PatientSignUpForm()
    context = {"uform": uform, "pform": pform}
    return render(request, "patient/signup.html", context)


def profile(request, pk):
    user = request.user
    patient = Patient.objects.get(id=pk)
    records = BookAppointment.objects.filter(doctor_id=pk)
    records = records[::-1]
    try:
        ispatient = user.patient.id
    except:
        ispatient = 0
    ### fetching review doctor form
    try:
        print("try chala")
        rating = request.GET["rating"]
        rating, record_id = rating.split("=")
        description = request.GET["description"]
    except:
        print("except chala")
        rating = description = None
    try:
        record = BookAppointment.objects.get(id=record_id)
    except:
        record = None
    print("YOYO", rating, description)
    if rating or description:
        print("YOYO", rating, description)
        obj = Review.objects.create()
        obj.rating = int(rating)
        obj.description = description
        obj.patient_id = patient.id
        obj.doctor_id = record.doctor_id
        obj.save()
    d = {
        "patient": patient,
        "records": records,
        "ispatient": ispatient,
    }
    return render(request, "patient/pat_profile.html", d)
