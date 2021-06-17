from django.shortcuts import render, HttpResponse
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Hospital
from .forms import HospitalSignUpForm, SearchHospitalForm
from home.models import Departments
from home.forms import UserSignUpForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout


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
                if filter_hos:
                    return HttpResponse(filter_hos)
                else:
                    return HttpResponse("No hsopital Found")
            if city_name:
                filter_doctors = Hospital.objects.filter(city=city_name)
                if filter_doctors:
                    return HttpResponse(filter_doctors)
                else:
                    return HttpResponse("No hospital found")
            if hos_name:
                filter_doctor = Hospital.objects.filter(user__username=hos_name)
                if filter_doctor:
                    return HttpResponse(filter_doctor)
                else:
                    return HttpResponse("No hospital found")
    d = {
        "hospitals": hospitals,
        "departments": departments,
        "user": request.user,
        "form": form,
    }
    return render(request, "hospital/hhome.html", d)


def hos_profile(request, pk):
    hospitul = Hospital.objects.get(id=pk)
    d = {"hospitals": hospitul}
    return render(request, "hospital/particular_hospital.html", d)


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
