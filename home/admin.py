from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(
    [Departments, Symptom, Disease, BookAppointment, Notification, DSEnrollment]
)
