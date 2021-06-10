from django.urls import path
from doctor import views
from django.shortcuts import render

urlpatterns = [
    path("signup", views.signup, name="dsignup"),
    path("exp", views.exp, name="exp"),
    path("dhome", views.dhome, name="dhome"),
]
