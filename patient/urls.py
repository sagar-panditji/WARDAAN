from django.urls import path
from patient import views
from django.shortcuts import render

urlpatterns = [
    path("signup", views.signup, name="psignup"),
]
