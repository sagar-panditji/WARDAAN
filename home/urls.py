from django.urls import path
from home import views
from django.shortcuts import render

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login, name="login"),
    path("exp", views.exp, name="exp"),
    path("blog", views.blogs, name="blogs"),
    path("ddepartment/<int:pk>", views.ddepartment, name="ddepartment"),
    path("hdepartment/<int:pk>", views.hdepartment, name="hdepartment"),
    path("departments", views.departments, name="departments"),
    path("dhome", views.doctor_home, name="dhome"),
    path("doctor/<int:pk>", views.doctor, name="doctor"),
    path("dlist", views.doctor_list, name="dlist"),
    path("hhome", views.hospital_home, name="hhome"),
    path("hospital/<int:pk>", views.hospital, name="hospital"),
    path("hlist", views.hospital_list, name="hlist"),
    path("add_d", views.add_disease, name="add_disease"),
    path("add_s", views.add_symptom, name="add_symptom"),
    path("disease/<int:pk>", views.disease, name="disease"),
    path("diseases", views.diseases, name="diseases"),
    path("book_appointment/<pk>", views.book_appointment_doc, name="book_appointment"),
]
