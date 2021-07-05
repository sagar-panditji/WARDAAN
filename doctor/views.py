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
from .models import Doctor, BookAppointment, Review
from .forms import (
    DoctorSignUpForm,
    SearchDoctorForm,
    CompareDoctor,
    BookAppointmentForm,
)
from home.models import Departments
from home.forms import UserSignUpForm
from home.views import (
    give_doctors_of_this_department,
    give_best_doctor_of_this_department,
    give_department_acc_to_symptoms,
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
    print("YOOOOOOOOOOOOOOOOOOOOO")
    if request.user.is_authenticated:
        try:
            if user.doctor:
                usertype["doc"] = 1
                doctor = user.doctor
                print("DDDDDD", doctor, type(doctor), doctor.user.username)
                records = BookAppointment.objects.filter(doctor_id=user.doctor.id)[::-1]
                #########
                try:
                    print("HOMEEE")
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
        except:
            print("PATIENTTTTTT")
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
        "usertype": usertype,
    }
    return render(request, "doctor/dhome.html", d)


def get_appointment_time(id):
    today = date.today()
    # SET APPOINTMENT FOR DOCTOR
    print("GET APPOITNMENT TIME")
    doctor = Doctor.objects.get(id=id)
    records = BookAppointment.objects.filter(
        appointment_date__gte=datetime.date.today()
    ).filter(doctor_id=id)
    print("RECORDS", records)
    open_time = str(doctor.open_time)
    close_time = str(doctor.close_time)
    print("OPEN-CLOSE", open_time, close_time)
    cnt = len(records)
    opne_hr = int(str(open_time)[:2])
    close_hr = int(str(close_time)[:2])
    if cnt % 2 == 0:
        print("IFFFFFF kai andar")
        opne_hr = opne_hr + (cnt // 2)
        print("OPENNNNNNN", opne_hr, close_hr)
        if opne_hr == close_hr:
            print("EEEEEEEEEEEEEEEEEEEEEEEEEEEE")
            print("QQQQQQQQQQQQ0", dt.time(00, 00, 00))
            return dt.time(00, 00, 00)
        appointment_time = dt.time(opne_hr, 00, 00)
        print("YOOOOOOO")
    else:
        print("ELSEEEEEE kai andar")
        opne_hr = opne_hr + (cnt // 2)
        if opne_hr == close_hr:
            return dt.time(00, 00, 00)
        appointment_time = dt.time(opne_hr, 30, 00)
    return appointment_time


@login_required(login_url="login")
def book_appointment_doc(request, pk):
    print("hello BOOK APPOINTMENT DOC", Doctor.objects.get(id=pk))
    departments = Departments.objects.all()
    if request.method == "POST":
        print("POST REQUEST")
        form = BookAppointmentForm(request.POST)
        print("CEHCKC  FORM")
        if form.is_valid():
            print("VALID FORMMMM")
            doctor = Doctor.objects.get(id=pk)
            patient = Patient.objects.get(id=request.user.patient.id)
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
            print("get appointment time")
            obj.appointment_time = get_appointment_time(obj.doctor_id)
            if obj.appointment_time == dt.time(00, 00, 00):
                return HttpResponse("Fully Booked")
            obj.save()
            print("HO GYI BOOK aPPOITNment")
            # logic ends
            dd = {}
            doc = Doctor.objects.get(id=pk)
            dd["doctor"] = doc
            dd["symptoms"] = obj.get_symptoms
            dd["description"] = obj.description
            dd["fees"] = doc.fees
            dd["time"] = obj.appointment_time
            print("TIMMMMEEEe", obj.appointment_time)
            dd["date"] = date.today()
            print("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD", dd)

            return render(request, "home/submitfees.html", dd)
        else:
            print("INVALID FORMMMM")
            print("FORM", form)
            return HttpResponse("invalid form")
    else:
        print("GET REQUEST")
        form = BookAppointmentForm()
    d = {"form": form, "departments": departments}
    return render(request, "home/book_appointment.html", d)


@login_required(login_url="login")
def find_me_a_doctor(request):
    user = request.user
    usertype = {"doc": 0, "pat": 0}
    print("YOOOOOOOOOOOOOOOOOOOOO")
    if request.user.is_authenticated:
        try:
            if user.doctor:
                usertype["doc"] = 1
                doctor = user.doctor
                print("DDDDDD", doctor, type(doctor), doctor.user.username)
                records = BookAppointment.objects.filter(doctor_id=user.doctor.id)[::-1]
                #########
                try:
                    print("HOMEEE")
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
        except:
            print("PATIENTTTTTT")
            usertype["pat"] = 1
            patient = user.patient
            records = BookAppointment.objects.filter(patient_id=user.patient.id)
    else:
        records = []
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
            print("get appointment time")
            obj.appointment_time = get_appointment_time(obj.doctor_id)
            if obj.appointment_time == dt.time(00, 00, 00):
                return HttpResponse("Fully Booked")
            obj.save()
            print("HO GYI BOOK aPPOITNment")
            # logic ends
            dd = {}
            dd["doctor"] = doctor
            dd["symptoms"] = obj.get_symptoms
            dd["description"] = obj.description
            dd["fees"] = doctor.fees
            dd["time"] = obj.appointment_time
            print("TIMMMMEEEe", obj.appointment_time)
            dd["date"] = date.today()
            print("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD", dd)
            return render(request, "home/submitfees.html", dd)
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
    print("YOOOOOOOOOOOOOOOOOOOOO")
    if request.user.is_authenticated:
        try:
            if user.doctor:
                usertype["doc"] = 1
                doctor = user.doctor
                print("DDDDDD", doctor, type(doctor), doctor.user.username)
                records = BookAppointment.objects.filter(doctor_id=user.doctor.id)[::-1]
                #########
                try:
                    print("HOMEEE")
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
        except:
            print("PATIENTTTTTT")
            usertype["pat"] = 1
            patient = user.patient
            records = BookAppointment.objects.filter(patient_id=user.patient.id)
    else:
        records = []
    department = Departments.objects.get(id=pk)
    departments = Departments.objects.all()
    doctors = give_doctors_of_this_department(department)
    if len(doctors) == 0:
        return HttpResponse("Currently there are no doctors in this department")
    d = {
        "doctors": doctors,
        "department": department,
        "departments": departments,
        "usertype": usertype,
    }
    return render(request, "home/ddepartment.html", d)


def doc_profile(request, pk):
    user = request.user
    doctor = Doctor.objects.get(id=pk)
    trecords = BookAppointment.objects.filter(doctor_id=pk).filter(
        appointment_date__gte=datetime.date.today()
    )
    for record in trecords:
        print(
            "LALALAL", record, record.patient_id, record.get_doctor, record.get_patient
        )
        if record.patient_img:
            print("IMAAAAAAGEEEEEEEEEEEEEEEEEEEEEEe", record.patient_img)
    today_appointment_cnt = len(
        BookAppointment.objects.filter(
            appointment_date__gte=datetime.date.today()
        ).filter(doctor_id=pk)
    )
    arecords = BookAppointment.objects.filter(doctor_id=pk)[::-1]
    reviews = Review.objects.all().filter(doctor_id=doctor.id)[::-1]
    print("ALL REVIEWS", Review.objects.all())
    print("REVIEWS", reviews)
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
    print("BLOG IDDD", doctor, doctor.user.id, user.id)
    blogs = Blogs.objects.all().filter(user=doctor.user)[::-1]
    print("BLOGSSSS", blogs)
    d = {
        "doctor": doctor,
        "trecords": trecords,
        "arecords": arecords,
        "today_appointment_cnt": today_appointment_cnt,
        "reviews": reviews,
        "blogs": blogs,
    }
    return render(request, "doctor/doc_profile.html", d)


def dlist(request):
    user = request.user
    usertype = {"doc": 0, "pat": 0}
    print("YOOOOOOOOOOOOOOOOOOOOO")
    if request.user.is_authenticated:
        try:
            if user.doctor:
                usertype["doc"] = 1
                doctor = user.doctor
                print("DDDDDD", doctor, type(doctor), doctor.user.username)
                records = BookAppointment.objects.filter(doctor_id=user.doctor.id)[::-1]
                #########
                try:
                    print("HOMEEE")
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
        except:
            print("PATIENTTTTTT")
            usertype["pat"] = 1
            patient = user.patient
            records = BookAppointment.objects.filter(patient_id=user.patient.id)
    else:
        records = []
    print("DDDDDLIIIIISTTTTTTT")
    doctors = Doctor.objects.all()
    d = {
        "doctors": doctors,
        "usertype": usertype,
    }
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
    user = request.user
    usertype = {"doc": 0, "pat": 0}
    print("YOOOOOOOOOOOOOOOOOOOOO")
    if request.user.is_authenticated:
        try:
            if user.doctor:
                usertype["doc"] = 1
                doctor = user.doctor
                print("DDDDDD", doctor, type(doctor), doctor.user.username)
                records = BookAppointment.objects.filter(doctor_id=user.doctor.id)[::-1]
                #########
                try:
                    print("HOMEEE")
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
        except:
            print("PATIENTTTTTT")
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
        print("DOC1", doc1, type(doc1))
        print("DOC2", doc2, type(doc2))
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
