from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Departments(models.Model):
    departments = [
        ("General Physician", "General Physician"),
        ("InfectiousDisease Physician", "InfectiousDisease Physician"),
        ("Anesthesiologists", "Anesthesiologists"),
        ("Pulmonologist", "Pulmonologist"),
        ("Cardiologist", "Cardiologist"),
        ("Neurologist", "Neurologist"),
        ("Allergists", "Allergists"),
        ("Dermatologists", "Dermatologists"),
        ("ayurveda", "ayurveda"),
        ("homoeopath", "homoeopath"),
        ("dentist", "dentist"),
    ]
    name = models.CharField(
        max_length=50, choices=departments, default="General Physician"
    )

    def __str__(self):
        return self.name


class Symptoms(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Disease(models.Model):
    name = models.CharField(max_length=100)
    symptoms = models.ManyToManyField(Symptoms)

    def __str__(self):
        return self.name


class BookAppointment(models.Model):
    CONFIRMED = 1
    CANCELLED = 2
    WAITING = 3
    STATUS_CODES = (
        (CONFIRMED, "Confirmed"),
        (CANCELLED, "Cancelled"),
        (WAITING, "Waiting"),
    )
    # token_no = models.IntegerField(null=True, blank=True)
    symptoms = models.ManyToManyField(Symptoms, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    appointment_date = models.DateField(auto_now=True, null=True, blank=True)
    status = models.PositiveSmallIntegerField(
        choices=STATUS_CODES, null=True, blank=True
    )
    """
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, null=True, blank=True
    )
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, null=True, blank=True
    )
    """


class Notification(models.Model):
    user_id = models.IntegerField(null=True, blank=True)
    message = models.CharField(max_length=1000, null=True, blank=True)
    read = models.BooleanField(default=False, null=True, blank=True)
