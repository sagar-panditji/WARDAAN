from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Departments(models.Model):
    departments = [
        ("Cardiologist", "Cardiologist"),
        ("Dermatologists", "Dermatologists"),
        ("Emergency Medicine Specialists", "Emergency Medicine Specialists"),
        ("Allergists/Immunologists", "Allergists/Immunologists"),
        ("Anesthesiologists", "Anesthesiologists"),
        ("Colon and Rectal Surgeons", "Colon and Rectal Surgeons"),
        ("pulmonologist", "pulmonologist"),
    ]
    name = models.CharField(max_length=50, choices=departments, default="Cardiologist")

    def __str__(self):
        return self.name
