from django.urls import path
from hospital import views
from django.shortcuts import render

urlpatterns = [
    path("signup", views.signup, name="signup"),
]
