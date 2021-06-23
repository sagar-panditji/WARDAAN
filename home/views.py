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
import datetime as dt
from datetime import datetime, timedelta, date
from django.conf import settings
from django.db.models import Q
from .forms import LoginForm, DiseaseForm, SymptomForm, BookAppointmentForm
from .models import Departments, Symptom, Disease, BookAppointment, AppointmentRecord
from doctor.models import Doctor
from patient.models import Patient
from hospital.models import Hospital
from django.contrib.auth.models import User


@login_required(login_url="login")
def exp(request):
    departments = Departments.objects.all()
    user = request.user
    d = {"departments": departments, "user": user}
    return render(request, "home/exp.html", d)


@login_required(login_url="login")
def home(request):
    user = request.user
    departments = Departments.objects.all()
    data = {}
    for department in departments:
        data[department] = give_doctors_of_this_department(
            department
        ) + give_hospitals_of_this_department(department)

    d = {"departments": departments, "data": data, "user": user}
    return render(request, "home/home.html", d)


def give_departments_of_symptoms(symptoms):
    departments = []
    d = {}
    for symptom in symptoms:
        d[disease] = 0
    for symptom in symptoms:
        for i in d.keys():
            if symptom in i.symptoms.all():
                d[i] += 1
    print(d)
    return departments


def give_doctors_of_this_department(department):
    l = []
    for doctor in Doctor.objects.all():
        if doctor.department == department:
            l.append(doctor)
    return l


def give_hospitals_of_this_department(department):
    l = []
    for hospital in Hospital.objects.all():
        if department in hospital.departments.all():
            l.append(hospital)
    return l


def give_doctors_of_this_department_of_this_hospital(department, hospital):
    doctors = []
    department = Departments.objects.get(name=department)
    for doctor in Doctor.objects.all():
        if doctor.department == department and doctor.hospital == hospital:
            doctors.append(doctor)
    return doctors


def app_record(request):
    today = date.today()
    records = AppointmentRecord.objects.filter(
        date__year=today.year, date__month=today.month, date__day=today.day
    ).filter(appointment__doctor_id=1)
    for record in records:
        print(record)
        print(record.appointment)
    print()
    d = {"departments": departments}
    return HttpResponse("ok")
    return render(request, "home/exp.html", d)


@login_required(login_url="login")
def departments(request):
    departments = Departments.objects.all()
    data = {}
    for department in departments:
        data[department] = give_doctors_of_this_department(
            department
        ) + give_hospitals_of_this_department(department)

    d = {"departments": departments, "data": data}
    return render(request, "home/departments.html", d)


def particular_department(request, pk):
    departments = Departments.objects.all()
    department = Departments.objects.get(id=pk)
    doctors = give_doctors_of_this_department(department)
    hospitals = give_hospitals_of_this_department(department)
    ld = len(doctors)
    lh = len(hospitals)
    d = {
        "department": department,
        "departments": departments,
        "doctors": doctors,
        "hospitals": hospitals,
        "ld": ld,
        "lh": lh,
    }
    return render(request, "home/particular_department.html", d)


# @login_required(login_url="login")
def diseases(request):
    diseases = Disease.objects.all()
    print("HELLO", diseases)
    d = {"diseases": diseases}
    return render(request, "home/diseases.html", d)


def disease(request, pk):
    try:
        obj = Disease.objects.get(id=pk)
        print(obj.name)
        print(obj.symptoms)
        return HttpResponse(obj)
    except:
        return HttpResponse("Id not found")


def add_disease(request):
    if request.method == "POST":
        form = DiseaseForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            disease = Disease.objects.create(name=name)
            for symptom in form.cleaned_data["symptoms"]:
                disease.symptoms.add(symptom)
            disease.save()
            #######
            print("name", disease.name)
            print("symptoms", disease.symptoms.all())
            return HttpResponse("ok")
        else:
            return HttpResponse("dhang se kar error hai")
    else:
        form = DiseaseForm()
    d = {"form": form}
    return render(request, "home/add_disease.html", d)


def add_symptom(request):
    if request.method == "POST":
        form = SymptomForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            symptom = Symptom.objects.create(name=name)
            return HttpResponse("ok")
    else:
        form = SymptomForm()
    d = {"form": form}
    return HttpResponse(Symptom.objects.all())
    return render(request, "home/add_symtoms.html", d)


@login_required(login_url="login")
def blogs(request):
    d = {}
    return HttpResponse("blogs")
    return render(request, "home/blog.html", d)


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
        return render(request, "home/login.html", d)


@login_required(login_url="login")
def logout(request):
    auth_logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("home")


"""
def is_admin(user):
    return user.groups.filter(name="ADMIN").exists()


def is_hospital(user):
    return user.groups.filter(name="HOSPITAL").exists()


def is_doctor(user):
    return user.groups.filter(name="DOCTOR").exists()


def is_patient(user):
    return user.groups.filter(name="PATIENT").exists()


def afterlogin_view(request):
    if is_patient(request.user):
        accountapproval = Patient.objects.all().filter(
            user_id=request.user.id, status=True
        )
        if accountapproval:
            return redirect("patient-dashboard")
        else:
            return render(request, "hospital/patient_wait_for_approval.html")
    elif is_doctor(request.user):
        accountapproval = Doctor.objects.all().filter(
            user_id=request.user.id, status=True
        )
        if accountapproval:
            return redirect("doctor-dashboard")
        else:
            return render(request, "hospital/doctor_wait_for_approval.html")
    else:
        accountapproval = Hospital.objects.all().filter(
            user_id=request.user.id, status=True
        )
        if accountapproval:
            return redirect("doctor-dashboard")
        else:
            return render(request, "hospital/doctor_wait_for_approval.html")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    # for both table in admin dashboard
    doctors = Doctor.objects.all().order_by("-id")
    patients = Patient.objects.all().order_by("-id")
    # for three cards
    doctorcount = Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount = Doctor.objects.all().filter(status=False).count()

    patientcount = Patient.objects.all().filter(status=True).count()
    pendingpatientcount = Patient.objects.all().filter(status=False).count()

    appointmentcount = Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount = Appointment.objects.all().filter(status=False).count()
    mydict = {
        "doctors": doctors,
        "patients": patients,
        "doctorcount": doctorcount,
        "pendingdoctorcount": pendingdoctorcount,
        "patientcount": patientcount,
        "pendingpatientcount": pendingpatientcount,
        "appointmentcount": appointmentcount,
        "pendingappointmentcount": pendingappointmentcount,
    }
    return render(request, "hospital/admin_dashboard.html", context=mydict)





@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def discharge_patient_view(request, pk):
    patient = Patient.objects.get(id=pk)
    days = date.today() - patient.admitDate  # 2 days, 0:00:00
    assignedDoctor = User.objects.all().filter(id=patient.assignedDoctorId)
    d = days.days  # only how many day that is 2
    patientDict = {
        "patientId": pk,
        "name": patient.get_name,
        "mobile": patient.mobile,
        "address": patient.address,
        "symptoms": patient.symptoms,
        "admitDate": patient.admitDate,
        "todayDate": date.today(),
        "day": d,
        "assignedDoctorName": assignedDoctor[0].first_name,
    }
    if request.method == "POST":
        feeDict = {
            "roomCharge": int(request.POST["roomCharge"]) * int(d),
            "doctorFee": request.POST["doctorFee"],
            "medicineCost": request.POST["medicineCost"],
            "OtherCharge": request.POST["OtherCharge"],
            "total": (int(request.POST["roomCharge"]) * int(d))
            + int(request.POST["doctorFee"])
            + int(request.POST["medicineCost"])
            + int(request.POST["OtherCharge"]),
        }
        patientDict.update(feeDict)
        # for updating to database patientDischargeDetails (pDD)
        pDD = PatientDischargeDetails()
        pDD.patientId = pk
        pDD.patientName = patient.get_name
        pDD.assignedDoctorName = assignedDoctor[0].first_name
        pDD.address = patient.address
        pDD.mobile = patient.mobile
        pDD.symptoms = patient.symptoms
        pDD.admitDate = patient.admitDate
        pDD.releaseDate = date.today()
        pDD.daySpent = int(d)
        pDD.medicineCost = int(request.POST["medicineCost"])
        pDD.roomCharge = int(request.POST["roomCharge"]) * int(d)
        pDD.doctorFee = int(request.POST["doctorFee"])
        pDD.OtherCharge = int(request.POST["OtherCharge"])
        pDD.total = (
            (int(request.POST["roomCharge"]) * int(d))
            + int(request.POST["doctorFee"])
            + int(request.POST["medicineCost"])
            + int(request.POST["OtherCharge"])
        )
        pDD.save()
        return render(request, "hospital/patient_final_bill.html", context=patientDict)
    return render(request, "hospital/patient_generate_bill.html", context=patientDict)


"""


"""
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def delete_patient_from_hospital_view(request, pk):
    patient = Patient.objects.get(id=pk)
    user = User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect("admin-view-patient")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def delete_doctor(request, pk):
    doctor = Doctor.objects.get(id=pk)
    user = User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect("admin-view-doctor")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def delete_hospital(request, pk):
    hospital = Hospital.objects.get(id=pk)
    user = User.objects.get(id=hospital.user_id)
    user.delete()
    hospital.delete()
    return redirect("admin-view-doctor")

"""
