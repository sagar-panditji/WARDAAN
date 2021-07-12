from django.shortcuts import render, redirect, HttpResponse
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
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from home.views import give_doctors_of_this_department
from home.models import Departments
from doctor.models import Doctor, BookAppointment
from patient.models import Patient
from blogs.models import *
from blogs.forms import *
from django.contrib.auth.models import User


def bhome(request):
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
    # accepting or rejecting appointments
    bdone = 1
    data = {}
    all_blogs = Blogs.objects.all()[::-1]
    departments = Departments.objects.all()
    b = Blogs()
    try:
        print("try chala of loadmore")
        loadmore = request.GET["loadmore"]
        b.load += 1
        if b.load * 5 >= len(all_blogs):
            b.load = 1
            blogs = all_blogs
        else:
            value = b.load * 5
            blogs = all_blogs[:value]
    except:
        print("except of loadmore")
        if len(all_blogs) <= 5:
            blogs = all_blogs
            bdone = 0
        else:
            blogs = all_blogs[:5]
    for department in departments:
        data[department] = give_doctors_of_this_department(department)
    d = {
        "departments": departments,
        "data": data,
        "user": user,
        "usertype": usertype,
        "records": records,
        "ln": len(blogs),
        "blogs": blogs,
        "bdone": bdone,
    }
    return render(request, "blogs/index.html", d)


def createblog(request):
    try:
        print("try chala")
        title = request.GET["title"]
        description = request.GET["desc"]
    except:
        title = description = None
        print("Except chala")
    if title and description:
        print("TITLE_AND_DESCRIPTION")
        obj = Blogs.objects.create(user=request.user)
        obj.user = request.user
        obj.title = title
        obj.description = description
        obj.save()
        return redirect("blogs")
    d = {}
    return render(request, "blogs/createblog.html", d)


def particular_blog(request, pk):
    user = request.user
    usertype = {"doc": 0, "pat": 0}
    blog = Blogs.objects.get(id=pk)
    departments = Departments.objects.all()
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
                d = {
                    "doctor": doctor,
                    "records": records,
                    "blog": blog,
                    "user": user,
                    "departments": departments,
                }
        except:
            print("PATIENTTTTTT")
            usertype["pat"] = 1
            patient = user.patient
            records = BookAppointment.objects.filter(patient_id=user.patient.id)
            d = {
                "patient": patient,
                "records": records,
                "blog": blog,
                "user": user,
                "departments": departments,
            }
    else:
        records = []
    return render(request, "blogs/particular_blog.html", d)
