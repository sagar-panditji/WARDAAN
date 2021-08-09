from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.conf import settings
from django.contrib.auth import (
    login,
    authenticate,
    login as auth_login,
    logout as auth_logout,
)
# decorator
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
    login_required,
)
from .models import Doctor, BookAppointment, Review
from .forms import (
    DoctorSignUpForm,
    SearchDoctorForm,
    CompareDoctor,
    BookAppointmentForm,
)
# import department and user sign up form
from home.models import Departments
from home.forms import UserSignUpForm
from home.views import (
    give_doctors_of_this_department,
    give_best_doctor_of_this_department,
    give_department_acc_to_symptoms,
    get_time,
)
from patient.models import Patient
from blogs.models import Blogs
from django.contrib.auth.models import User
import datetime as dt
import datetime
from datetime import timedelta, date
from django.conf import settings
from django.db.models import Q
from django.core.mail import send_mail


def doc_exp(request):
    department = Departments.objects.get(id=1)
    doctors = Doctor.objects.all()
    d = {"doctors": doctors}
    return render(request, "doctor/exp.html", d)


def doc_home(request):
    user = request.user
    usertype = {"doc": 0, "pat": 0}
    # if user alredy exist, then book appointment
    if request.user.is_authenticated:
        try:
            if user.doctor:
                usertype["doc"] = 1
                doctor = user.doctor
                records = BookAppointment.objects.filter(doctor_id=user.doctor.id)[::-1]
                #########
                try:
                    status = request.GET["aor"]
                    record_id = int(status[:-1])
                    record = BookAppointment.objects.get(id=record_id)
                    if status[-1] == "a":
                        record.status = 1
                        record.save()
                    else:
                        record.delete()
                except:
                    status = None
                d = {"doctor": doctor, "records": records}
        except:
            usertype["pat"] = 1
            patient = user.patient
            records = BookAppointment.objects.filter(patient_id=user.patient.id)
    else:
        records = []
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
            # if city name found, then return city name else return "No result found"
            if city_name:
                filter_doctors = Doctor.objects.filter(city=city_name)
                if not filter_doctors:
                    return HttpResponse("No doctor found")
            if doctor_name:
                filter_doctors = Doctor.objects.filter(user__username=doctor_name)
                if not filter_doctors:
                    return HttpResponse("No doctor found")
            d = {
                "doctors": filter_doctors,
                "departments": Departments.objects.all(),
                "blogs": Blogs.objects.all(),
                "user": request.user,
                "usertype": usertype,
            }
            print("DLISSSTTTTTTTT")
            return render(request, "doctor/dlist.html", d)
    d = {
        "doctors": doctors,
        "departments": departments,
        "user": request.user,
        "form": form,
        "usertype": usertype,
    }
    return render(request, "doctor/dhome.html", d)


def get_appointment_time(id):
    today = date.today()
    # SET APPOINTMENT FOR DOCTOR
    doctor = Doctor.objects.get(id=id)
    records = BookAppointment.objects.filter(
        appointment_date__gte=datetime.date.today()
    ).filter(doctor_id=id)
    cnt = len(records)
    open_time = str(doctor.open_time)
    close_time = str(doctor.close_time)
    opne_hr = int(str(open_time)[:2])
    close_hr = int(str(close_time)[:2])
    ### finding current time and hour
    current_time = datetime.datetime.now()
    current_hr = current_time.hour
    current_min = current_time.minute
    open_time_hr, open_time_min = get_time(open_time)
    close_time_hr, close_time_min = get_time(close_time)
    if current_hr > close_time_hr:
        return dt.time(00, 00, 00)
    if current_hr > open_time_hr:
        opne_hr = current_hr + 1
        if opne_hr > close_hr:
            return dt.time(00, 00, 00)
    if cnt % 2 == 0:
        opne_hr = opne_hr + (cnt // 2)
        if opne_hr == close_hr:
            return dt.time(00, 00, 00)
        appointment_time = dt.time(opne_hr, 00, 00)
    else:
        opne_hr = opne_hr + (cnt // 2)
        if opne_hr == close_hr:
            return dt.time(00, 00, 00)
        appointment_time = dt.time(opne_hr, 30, 00)
    return appointment_time


@login_required(login_url="login")
def book_appointment_doc(request, pk):
    user = request.user
    usertype = {"doc": 0, "pat": 0}
    if request.user.is_authenticated:
        try:
            if user.doctor:
                usertype["doc"] = 1
        except:
            usertype["pat"] = 1
    if usertype["doc"]:
        return HttpResponse("You have to be a patient to book appointment")
    departments = Departments.objects.all()
    if request.method == "POST":
        form = BookAppointmentForm(request.POST)
        if form.is_valid():
            doctor = Doctor.objects.get(id=pk)
            try:
                patient = Patient.objects.get(id=request.user.patient.id)
            except:
                return HttpResponse("You have to be a patient to book appointment")
            obj = BookAppointment.objects.create()
            obj.description = form.cleaned_data["description"]
            symptoms = form.cleaned_data["symptoms"]
            for symptom in form.cleaned_data["symptoms"]:
                obj.symptoms.add(symptom)
            obj.doctor_id = pk
            try:
                obj.patient_id = request.user.patient.id
                obj.patient_img = patient.profile_pic
                obj.doctor_img = doctor.profile_pic
            except:
                return HttpResponse("You have to be a patient to book appointment ")
            # Appointment time konsa milega patient ko
            obj.appointment_time = get_appointment_time(obj.doctor_id)
            if obj.appointment_time == dt.time(00, 00, 00):
                return HttpResponse("Fully Booked")
            obj.save()
            # logic ends
            return redirect("home")
        else:
            return HttpResponse("invalid form")
    else:
        form = BookAppointmentForm()
    d = {"form": form, "departments": departments}
    return render(request, "home/book_appointment.html", d)


@login_required(login_url="login")
def find_me_a_doctor(request):
    user = request.user
    usertype = {"doc": 0, "pat": 0}
    if request.user.is_authenticated:
        try:
            if user.doctor:
                usertype["doc"] = 1
                doctor = user.doctor
                records = BookAppointment.objects.filter(doctor_id=user.doctor.id)[::-1]
                #########
                try:
                    status = request.GET["aor"]
                    record_id = int(status[:-1])
                    record = BookAppointment.objects.get(id=record_id)
                    if status[-1] == "a":
                        record.status = 1
                        record.save()
                    else:
                        record.delete()
                except:
                    status = None
                d = {"doctor": doctor, "records": records}
        except:
            usertype["pat"] = 1
            patient = user.patient
            records = BookAppointment.objects.filter(patient_id=user.patient.id)
    else:
        records = []
    if usertype["doc"]:
        return HttpResponse("You have to be a patient to book appointment")
    departments = Departments.objects.all()
    if request.method == "POST":
        form = BookAppointmentForm(request.POST)
        if form.is_valid():
            obj = BookAppointment.objects.create()
            obj.description = form.cleaned_data["description"]
            symptoms = form.cleaned_data["symptoms"]
            for symptom in form.cleaned_data["symptoms"]:
                obj.symptoms.add(symptom)
            department = give_department_acc_to_symptoms(symptoms)
            if department == None:
                return HttpResponse("Please Add Departments First !!")
            doctor = give_best_doctor_of_this_department(department)
            obj.doctor_img = doctor.profile_pic
            try:
                obj.doctor_id = doctor.id
            except:
                return HttpResponse("Sorry!! Couldn't find a doctor for you")
            try:
                patient = Patient.objects.get(id=request.user.patient.id)
                obj.patient_id = request.user.patient.id
                obj.patient_img = patient.profile_pic
            except:
                return HttpResponse("You have to be a patient to book appointment ")
            obj.appointment_time = get_appointment_time(obj.doctor_id)
            if obj.appointment_time == dt.time(00, 00, 00):
                return HttpResponse("Fully Booked")
            obj.save()
            # logic ends
            return redirect("home")
        else:
            print("FORM", form)
            return HttpResponse("invalid form")
    else:
        form = BookAppointmentForm()
    d = {"form": form, "departments": departments, "usertype": usertype}
    return render(request, "home/book_appointment.html", d)


def ddepartment(request, pk):
    user = request.user
    usertype = {"doc": 0, "pat": 0}
    if request.user.is_authenticated:
        try:
            if user.doctor:
                usertype["doc"] = 1
                doctor = user.doctor
                records = BookAppointment.objects.filter(doctor_id=user.doctor.id)[::-1]
                #########
                try:
                    status = request.GET["aor"]
                    record_id = int(status[:-1])
                    record = BookAppointment.objects.get(id=record_id)
                    if status[-1] == "a":
                        record.status = 1
                        record.save()
                    else:
                        record.delete()
                except:
                    status = None
                d = {"doctor": doctor, "records": records}
        except:
            usertype["pat"] = 1
            patient = user.patient
            records = BookAppointment.objects.filter(patient_id=user.patient.id)
    else:
        records = []
    department = Departments.objects.get(id=pk)
    departments = Departments.objects.all()
    doctors = give_doctors_of_this_department(department)
    d = {
        "doctors": doctors,
        "department": department,
        "departments": departments,
        "usertype": usertype,
        "ld": len(doctors),
    }
    return render(request, "home/ddepartment.html", d)


def doc_profile(request, pk):
    print("dOCCCCC PRIFLEEEEE")
    user = request.user
    doctor = Doctor.objects.get(id=pk)
    trecords = BookAppointment.objects.filter(doctor_id=pk).filter(
        appointment_date__gte=datetime.date.today()
    )
    today_appointment_cnt = len(
        BookAppointment.objects.filter(
            appointment_date__gte=datetime.date.today()
        ).filter(doctor_id=pk)
    )
    arecords = BookAppointment.objects.filter(doctor_id=pk)[::-1]
    reviews = Review.objects.all().filter(doctor_id=doctor.id)[::-1]
    try:
        status = request.GET["aor"]
        record_id = int(status[:-1])
        record = BookAppointment.objects.get(id=record_id)
        if status[-1] == "a":
            record.status = 1
            record.save()
        else:
            record.delete()
    except:
        status = None
    blogs = Blogs.objects.all().filter(user=doctor.user)[::-1]
    d = {
        "doctor": doctor,
        "trecords": trecords,
        "arecords": arecords,
        "today_appointment_cnt": today_appointment_cnt,
        "reviews": reviews,
        "blogs": blogs,
    }
    return render(request, "doctor/doc_profile.html", d)

# function defined for doctor list
def dlist(request):
    print("HELOOOOOO")
    user = request.user
    usertype = {"doc": 0, "pat": 0}
    if request.user.is_authenticated:
        try:
            if user.doctor:
                usertype["doc"] = 1
                doctor = user.doctor
                records = BookAppointment.objects.filter(doctor_id=user.doctor.id)[::-1]
                #########
                try:
                    status = request.GET["aor"]
                    record_id = int(status[:-1])
                    record = BookAppointment.objects.get(id=record_id)
                    if status[-1] == "a":
                        record.status = 1
                        record.save()
                    else:
                        record.delete()
                except:
                    status = None
                d = {"doctor": doctor, "records": records}
        except:
            usertype["pat"] = 1
            patient = user.patient
            records = BookAppointment.objects.filter(patient_id=user.patient.id)
    else:
        records = []
    doctors = Doctor.objects.all()
    d = {
        "doctors": doctors,
        "usertype": usertype,
    }
    return render(request, "doctor/dlist.html", d)

# this function defined for doctor sign up
def doc_signup(request):
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
            # set logic ends
            for dgr in dform.cleaned_data["degree"]:
                doctor.degree.add(dgr)
            doctor.save()
            return redirect("home")
        else:
            return HttpResponse("unmatched password or invalid form")
    else:
        uform = UserSignUpForm()
        dform = DoctorSignUpForm()
    context = {"uform": uform, "dform": dform}
    return render(request, "doctor/signup.html", context)

# Function defined for comparison of doctors
def comparison_doc(request):
    user = request.user
    usertype = {"doc": 0, "pat": 0}
    if request.user.is_authenticated:
        try:
            if user.doctor:
                usertype["doc"] = 1
                doctor = user.doctor
                records = BookAppointment.objects.filter(doctor_id=user.doctor.id)[::-1]
                #########
                try:
                    status = request.GET["aor"]
                    record_id = int(status[:-1])
                    record = BookAppointment.objects.get(id=record_id)
                    if status[-1] == "a":
                        record.status = 1
                        record.save()
                    else:
                        record.delete()
                except:
                    status = None
                d = {"doctor": doctor, "records": records}
        except:
            usertype["pat"] = 1
            patient = user.patient
            records = BookAppointment.objects.filter(patient_id=user.patient.id)
    else:
        records = []
    doctors = Doctor.objects.all()
    departments = Departments.objects.all()
    try:
        doc1 = request.GET["doc1"]
        doc2 = request.GET["doc2"]
    except:
        doc1 = doc2 = None
    if doc1 and doc2:
        doc1 = Doctor.objects.get(id=int(doc1))
        doc2 = Doctor.objects.get(id=int(doc2))
        d = {
            "doc1": doc1,
            "doc2": doc2,
            "departments": departments,
            "usertype": usertype,
        }
        return render(request, "doctor/comparedocs.html", d)
    else:
        print("yoyo")
    d = {
        "doctors": doctors,
        "usertype": usertype,
    }
    return render(request, "doctor/compareform.html", d)
