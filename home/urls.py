from django.urls import path
from home import views
from django.shortcuts import render

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login, name="login"),
    path("exp", views.exp, name="exp"),
    path("blog", views.blogs, name="blogs"),
    path("department/<str:department>", views.department, name="department"),
    path("department_list", views.department_list, name="department_list"),
    path("dhome", views.doctor_home, name="dhome"),
    path("doctor/<int:pk>", views.doctor, name="doctor"),
    path("dlist", views.doctor_list, name="dlist"),
    path("hhome", views.hospital_home, name="hhome"),
    path("hospital/<int:pk>", views.hospital, name="hospital"),
    path("hlist", views.hospital_list, name="hlist"),
    path("diseases", views.diseases, name="diseases"),
    path("add_disease", views.add_disease, name="add_disease"),
]
