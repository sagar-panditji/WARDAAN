from django.urls import path
from home import views
from doctor import views as dv
from patient import views as pv
from blogs import views as bv
from django.shortcuts import render

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
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
    path("find_me_a_doc", dv.find_me_a_doctor, name="find_doc"),
    path("ddepartment/<int:pk>", dv.ddepartment, name="ddepartment"),
    path("doc_profile/<int:pk>", dv.doc_profile, name="doc_profile"),
    path(
        "book_appointment_doc/<int:pk>",
        dv.book_appointment_doc,
        name="book_appointment_doc",
    ),
    path("comparison_doc", dv.comparison_doc, name="comparison_doc"),
    # Patient Views
    path("pat_profile/<int:pk>", pv.profile, name="pat_profile"),
    # Blogs Views
    path("blogs", bv.bhome, name="blogs"),
    path("create", bv.createblog, name="createb"),
    path("blog/<int:pk>", bv.particular_blog, name="particular_blog"),
]
