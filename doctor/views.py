from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.conf import settings
from django.contrib.auth import (
    login,
    authenticate,
    login as auth_login,
    logout as auth_logout,
)
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
    login_required,
)
from .models import Doctor
from .forms import DoctorSignUpForm, SearchDoctorForm, CompareDoctor
from home.models import Departments, BookAppointment, AppointmentRecord
from home.forms import UserSignUpForm, BookAppointmentForm
from home.views import (
    give_doctors_of_this_department,
    give_hospitals_of_this_department,
    give_doctors_of_this_department_of_this_hospital,
)
from django.contrib.auth.models import User
import datetime as dt
from datetime import datetime, timedelta, date
from django.conf import settings
from django.db.models import Q


def doc_exp(request):
    department = Departments.objects.get(id=1)
    doctors = Doctor.objects.all()
    d = {"doctors": doctors}
    return render(request, "doctor/exp.html", d)


def doc_home(request):
    doctors = Doctor.objects.all()
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
                if not filter_doctors:
                    return HttpResponse("No Doctor Found")
            if city_name:
                filter_doctors = Doctor.objects.filter(city=city_name)
                if not filter_doctors:
                    return HttpResponse("No doctor found")
            if doctor_name:
                filter_doctors = Doctor.objects.filter(user__username=doctor_name)
                if not filter_doctors:
                    return HttpResponse("No doctor found")
            d = {"doctors": filter_doctors, "departments": Departments.objects.all()}
            return render(request, "doctor/dlist.html", d)
    d = {
        "doctors": doctors,
        "departments": departments,
        "user": request.user,
        "form": form,
    }
    return render(request, "doctor/dhome.html", d)


def get_appointment_time_doc(id):
    today = date.today()
    # SET APPOINTMENT FOR DOCTOR
    doctor = Doctor.objects.get(id=id)
    records = AppointmentRecord.objects.filter(
        date__year=today.year, date__month=today.month, date__day=today.day
    ).filter(appointment__doctor_id=id)
    open_time = str(doctor.open_time)
    close_time = str(doctor.close_time)
    cnt = len(records)
    hour = int(str(open_time)[:2])
    print("HHH", hour)
    if cnt % 2 == 0:
        hour = hour + (cnt // 2)
        appointment_time = dt.time(hour, 00, 00)
    else:
        hour = hour + (cnt // 2)
        appointment_time = dt.time(hour, 30, 00)
    print("DDD", appointment_time)
    return appointment_time


@login_required(login_url="login")
def book_appointment_doc(request, pk):
    print("BOOK APPOINTMENT DOC")
    print("PKKKKKK", pk)
    print("DDDDDD", Doctor.objects.get(id=pk))
    departments = Departments.objects.all()
    if request.method == "POST":
        form = BookAppointmentForm(request.POST)
        if form.is_valid():
            obj = BookAppointment.objects.create()
            obj.description = form.cleaned_data["description"]
            symptoms = form.cleaned_data["symptoms"]
            for symptom in form.cleaned_data["symptoms"]:
                obj.symptoms.add(symptom)
            obj.doctor_id = pk
            obj.patient_id = request.user.id
            obj.save()
            record = AppointmentRecord.objects.create()
            record.appointment = obj
            record.date = obj.appointment_date
            record.save()
            # Appointment time konsa milega patient ko
            obj.appointment_time = get_appointment_time_doc(obj.doctor_id)
            obj.save()
            # logic ends
            return HttpResponse("your appointment has been successfully submitted")
        else:
            print("FORM", form)
            return HttpResponse("invalid form")
    else:
        form = BookAppointmentForm()
    d = {"form": form, "departments": departments}
    return render(request, "home/book_appointment.html", d)


@login_required(login_url="login")
def find_me_a_doctor(request):
    print("Find me a  DOC")
    return HttpResponse("under working")
    departments = Departments.objects.all()
    if request.method == "POST":
        form = BookAppointmentForm(request.POST)
        if form.is_valid():
            obj = BookAppointment.objects.create()
            obj.description = form.cleaned_data["description"]
            symptoms = form.cleaned_data["symptoms"]
            for symptom in form.cleaned_data["symptoms"]:
                obj.symptoms.add(symptom)
            obj.doctor_id = 1
            obj.patient_id = request.user.id
            obj.save()
            record = AppointmentRecord.objects.create()
            record.appointment = obj
            record.date = obj.appointment_date
            record.save()
            # Appointment time konsa milega patient ko
            obj.appointment_time = get_appointment_time_doc(obj.doctor_id)
            obj.save()
            # logic ends
            return HttpResponse("your appointment has been successfully submitted")
        else:
            print("FORM", form)
            return HttpResponse("invalid form")
    else:
        form = BookAppointmentForm()
    d = {"form": form, "departments": departments}
    return render(request, "home/book_appointment.html", d)


def ddepartment(request, pk):
    department = Departments.objects.get(id=pk)
    departments = Departments.objects.all()
    doctors = give_doctors_of_this_department(department)
    if len(doctors) == 0:
        return HttpResponse("Currently there are no doctors in this department")
    d = {
        "doctors": doctors,
        "department": department,
        "departments": departments,
    }
    return render(request, "home/ddepartment.html", d)


def doc_profile(request, pk):
    doctor = Doctor.objects.get(id=pk)
    records = BookAppointment.objects.filter(doctor_id=pk)
    records = records[::-1]
    try:
        status = request.GET["aor"]
        record_id = int(status[:-1])
        print("STATUS", status)
        record = BookAppointment.objects.get(id=record_id)
        if status[-1] == "a":
            print("BEFORE", record.status)
            record.status = 1
            record.save()
            print("AFTER", record.status)
        else:
            record.delete()
    except:
        status = None
    d = {"doctor": doctor, "records": records}
    return render(request, "doctor/doc_profile.html", d)


def dlist(request):
    doctors = Doctor.objects.all()
    d = {"doctors": doctors}
    return render(request, "doctor/dlist.html", d)


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
            user.set_password(user.password)
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
            hospital = dform.cleaned_data["hospital"]
            doctor.hospital = hospital
            # set the department of this doctor into the department of this hospital
            if hospital:
                for dept in hospital.departments.all():
                    if dept == doctor.department:
                        break
                else:
                    hospital.departments.add(doctor.department)
                hospital.save()
            doctor.save()
            # set logic ends
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


def comparison_doc(request):
    doctors = Doctor.objects.all()
    departments = Departments.objects.all()
    try:
        doc1 = request.GET["doc1"]
        doc2 = request.GET["doc2"]
    except:
        doc1 = doc2 = None
    if doc1 and doc2:
        print("DOC1", doc1, type(doc1))
        print("DOC2", doc2, type(doc2))
        doc1 = Doctor.objects.get(id=int(doc1))
        doc2 = Doctor.objects.get(id=int(doc2))
        d = {"doc1": doc1, "doc2": doc2, "departments": departments}
        return render(request, "doctor/comparedocs.html", d)
    else:
        print("yoyo")
    d = {"doctors": doctors}
    return render(request, "doctor/compareform.html", d)
