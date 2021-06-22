from django.urls import path
from home import views
from doctor import views as dv
from hospital import views as hv
from patient import views as pv
from django.shortcuts import render

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login, name="login"),
    path("exp", views.exp, name="exp"),
    path("add_d", views.add_disease, name="add_disease"),
    path("add_s", views.add_symptom, name="add_symptom"),
    path("disease/<int:pk>", views.disease, name="disease"),
    path("diseases", views.diseases, name="diseases"),
    # Department views
    path("departments", views.departments, name="departments"),
    path(
        "department/<int:pk>", views.particular_department, name="particular_department"
    ),
    # Doctor Views
    path("dhome", dv.doc_home, name="dhome"),
    path("dlist", dv.dlist, name="dlist"),
    path("dsignup", dv.doc_signup, name="dsignup"),
    path("find_me_a_doc", dv.find_me_a_doctor, name="find_me_a_doc"),
    path("ddepartment/<int:pk>", dv.ddepartment, name="ddepartment"),
    path("doc_profile/<int:pk>", dv.doc_profile, name="doc_profile"),
    path(
        "book_appointment_doc/<int:pk>",
        dv.book_appointment_doc,
        name="book_appointment_doc",
    ),
    # hospital Views
    path("hhome", hv.hos_home, name="hhome"),
    path("hsignup", hv.hos_signup, name="hsignup"),
    path("hdepartment/<int:pk>", hv.hdepartment, name="hdepartment"),
    path("hos_profile/<int:pk>", hv.hos_profile, name="hos_profile"),
    path("find_me_a_hos", hv.find_me_a_hospital, name="find_me_a_hos"),
    path("ba_hos_direct/<int:pk>", hv.ba_hos_direct, name="ba_hos_direct"),
    path(
        "book_appointment_hos/<int:pk>/<department>",
        hv.book_appointment_hos,
        name="book_appointment_hos",
    ),
    # Blogs Views
    path("blog", views.blogs, name="blogs"),
]
