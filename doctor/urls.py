from django.urls import path
from doctor import views
from django.shortcuts import render

urlpatterns = [
    path("dexp", views.doc_exp, name="dexp"),
    path("card", views.best_card),
]
