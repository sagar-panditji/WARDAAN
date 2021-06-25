from django.shortcuts import render, HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
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
from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Hospital
from .forms import HospitalSignUpForm, SearchHospitalForm
from home.models import Departments, BookAppointment, AppointmentRecord
from home.forms import UserSignUpForm, BookAppointmentForm
from home.views import (
    give_hospitals_of_this_department,
    give_doctors_of_this_department_of_this_hospital,
)
from django.contrib.auth.models import User
import datetime as dt
from datetime import datetime, timedelta, date
from django.conf import settings
from django.db.models import Q


def exp(request):
    departments = Departments.objects.all()
    hospitals = Hospital.objects.all()
    d = {"hospitals": hospitals, "departments": departments}
    return render(request, "hospital/exp.html", d)


def hos_home(request):
    departments = Departments.objects.all()
    hospitals = Hospital.objects.all()
    form = SearchHospitalForm()
    if request.method == "POST":
        form = SearchHospitalForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data["city"]
            hos_name = form.cleaned_data["hospital"]
            if city_name and hos_name:
                filter_hos = Hospital.objects.filter(city=city_name).filter(
                    user__username=hos_name
                )
                if not filter_hos:
                    return HttpResponse("No hsopital Found")
            if city_name:
                filter_hos = Hospital.objects.filter(city=city_name)
                if not filter_hos:
                    return HttpResponse("No hospital found")
            if hos_name:
                filter_hos = Hospital.objects.filter(user__username=hos_name)
                if not filter_hos:
                    return HttpResponse("No hospital found")
            d = {"hospitals": filter_hos, "departments": Departments.objects.all()}
            return render(request, "hospital/hlist.html", d)
    d = {
        "hospitals": hospitals,
        "departments": departments,
        "user": request.user,
        "form": form,
    }
    return render(request, "hospital/hhome.html", d)


def hos_profile(request, pk):
    hospital = Hospital.objects.get(id=pk)
    records = BookAppointment.objects.filter(hospital_id=pk)
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
    departments = hospital.departments.all()
    d = {"hospital": hospital, "records": records, "departments": departments}
    return render(request, "hospital/hos_profile.html", d)


def get_appointment_time_hos(id, department):
    print("GET APPOINMTNT TIME HOS")
    today = date.today()
    hospital = Hospital.objects.get(id=id)
    doctors = give_doctors_of_this_department_of_this_hospital(department, hospital)
    print("YOYO", "DOCTORS", doctors)
    counts = []
    if doctors == []:
        return None
    for doctor in doctors:
        records = AppointmentRecord.objects.filter(
            date__year=today.year, date__month=today.month, date__day=today.day
        ).filter(appointment__doctor_id=doctor.id)
        counts.append(len(records))
        print("DOC_RECORDS", doctor, records)
    # SET APPOINTMENT TIME
    def give_next_doctor():
        value = counts[0]
        for i in range(len(counts)):
            if counts[i] != value:
                return i
        return 0

    ind = give_next_doctor()
    doctor = doctors[ind]
    open_time = str(doctor.open_time)
    close_time = str(doctor.close_time)
    cnt = counts[ind]
    hour = int(str(open_time)[:2])
    print("HHH", hour)
    if cnt % 2 == 0:
        hour = hour + (cnt // 2)
        appointment_time = dt.time(hour, 00, 00)
    else:
        hour = hour + (cnt // 2)
        appointment_time = dt.time(hour, 30, 00)
    print("TIME", appointment_time)
    return appointment_time, doctors[ind].id


def book_appointment_hos(request, pk, department=None):
    print("BOOK APPOINTMENT HOS", pk)
    if request.method == "POST":
        form = BookAppointmentForm(request.POST)
        if form.is_valid():
            obj = BookAppointment.objects.create()
            obj.description = form.cleaned_data["description"]
            symptoms = form.cleaned_data["symptoms"]
            for symptom in form.cleaned_data["symptoms"]:
                obj.symptoms.add(symptom)
            obj.save()
            # Getting Appointment time for patient
            doctors = give_doctors_of_this_department_of_this_hospital(
                department, Hospital.objects.get(id=pk)
            )
            if doctors == []:
                return HttpResponse("No doctors in this department")
            appointment_time, doctor_id = get_appointment_time_hos(pk, department)
            obj.appointment_time = appointment_time
            obj.hospital_id = pk
            obj.doctor_id = doctor_id
            obj.patient_id = request.user.id
            obj.save()
            # logic ends
            record = AppointmentRecord.objects.create()
            record.appointment = obj
            record.date = obj.appointment_date
            record.save()
            return HttpResponse("your appointment has been successfully submitted")
        else:
            print("FORM", form)
            return HttpResponse("invalid form")
    else:
        form = BookAppointmentForm()
    d = {"form": form}
    return render(request, "home/book_appointment.html", d)


def find_me_a_hospital(request):
    return HttpResponse("under working")


def ba_hos_direct(request, pk):
    print("BOOK APPOINTMENT HOS Direct", pk)
    if request.method == "POST":
        form = BookAppointmentForm(request.POST)
        if form.is_valid():
            obj = BookAppointment.objects.create()
            obj.description = form.cleaned_data["description"]
            symptoms = form.cleaned_data["symptoms"]
            for symptom in form.cleaned_data["symptoms"]:
                obj.symptoms.add(symptom)
            obj.save()
            # Getting Appointment time for patient
            department = Departments.objects.get(name="General Physician")
            doctors = give_doctors_of_this_department_of_this_hospital(
                department, Hospital.objects.get(id=pk)
            )
            if doctors == []:
                return HttpResponse("No doctors in this department")
            ### ye uppar boundary condtn check ki , whether this hodspital has doctors in this department
            appointment_time, doctor_id = get_appointment_time_hos(pk, department)
            obj.appointment_time = appointment_time
            obj.hospital_id = pk
            obj.doctor_id = doctor_id
            obj.patient_id = request.user.id
            obj.save()
            # logic ends
            record = AppointmentRecord.objects.create()
            record.appointment = obj
            record.date = obj.appointment_date
            record.save()
            return HttpResponse("your appointment has been successfully submitted")
        else:
            print("FORM", form)
            return HttpResponse("invalid form")
    else:
        form = BookAppointmentForm()
    d = {"form": form}
    return render(request, "home/book_appointment.html", d)


@login_required(login_url="login")
def hdepartment(request, pk):
    department = Departments.objects.get(id=pk)
    departments = Departments.objects.all()
    hospitals = give_hospitals_of_this_department(department)
    print("Hdepartment", pk, department)
    if len(hospitals) == 0:
        return HttpResponse("Currently there are no hospitals in this department")
    d = {
        "hospitals": hospitals,
        "department": department,
        "departments": departments,
    }
    return render(request, "home/hdepartment.html", d)


def hos_list(request):
    hospitals = Hospital.objects.all()
    d = {"hospitals": hospitals}
    return render(request, "hospital/hlist.html", d)


def hos_signup(request):
    if request.method == "POST":
        uform = UserSignUpForm(request.POST)
        hform = HospitalSignUpForm(request.POST)
        if uform.is_valid() and hform.is_valid():
            ### Creating User ###
            user = uform.save()
            user.first_name = uform.cleaned_data["first_name"]
            user.last_name = uform.cleaned_data["last_name"]
            user.username = uform.cleaned_data["username"]
            user.email = uform.cleaned_data["email"]
            user.password = uform.cleaned_data["password"]
            user.set_password(user.password)
            user.save()
            ### Creating Hospital ###
            hospital = hform.save(commit=False)
            hospital.user = user
            hospital.mobile = hform.cleaned_data["mobile"]
            hospital.address = hform.cleaned_data["address"]
            hospital.city = hform.cleaned_data["city"]
            hospital.state = hform.cleaned_data["state"]
            hospital.no_of_beds = hform.cleaned_data["no_of_beds"]
            hospital.save()
            ### ye departments aache se kaam nhi kr rhe
            for department in hform.cleaned_data["departments"]:
                hospital.departments.add(department)
            hospital.save()
            print("departments", hospital.departments.all())
            return HttpResponse("ok")
        else:
            return HttpResponse("unmatched password or invalid form")
    else:
        uform = UserSignUpForm()
        hform = HospitalSignUpForm()
    context = {"uform": uform, "hform": hform}
    return render(request, "hospital/signup.html", context)


def comparison_hos(request):
    hospitals = Hospital.objects.all()
    departments = Departments.objects.all()
    try:
        hos1 = request.GET["hos1"]
        hos2 = request.GET["hos2"]
    except:
        hos1 = hos2 = None
    if hos1 and hos2:
        print("hos1", hos1, type(hos1))
        print("hos2", hos2, type(hos2))
        hos1 = Hospital.objects.get(id=int(hos1))
        hos2 = Hospital.objects.get(id=int(hos2))
        d = {"hos1": hos1, "hos2": hos2, "departments": departments}
        return render(request, "hospital/comparehos.html", d)
    else:
        print("yoyo")
    d = {"hospitals": hospitals}
    return render(request, "hospital/compareform.html", d)
