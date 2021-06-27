from django.db import models
from django.contrib.auth.models import User
import patient, doctor

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
        ("Ayurveda", "Ayurveda"),
        ("Homoeopath", "Homoeopath"),
        ("Dentist", "Dentist"),
    ]
    name = models.CharField(
        max_length=50, choices=departments, default="General Physician"
    )
    about = models.CharField(max_length=512, null=True, blank=True)
    url = models.URLField(
        max_length=250,
        default="https://www.imsanz.org.au/about-us/what-is-a-general-physician",
    )

    def __str__(self):
        return self.name


class Symptom(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Disease(models.Model):
    name = models.CharField(max_length=100)
    symptoms = models.ManyToManyField(Symptom)

    def __str__(self):
        return self.name


class BookAppointment(models.Model):
    CONFIRMED = 1
    CANCELLED = 2
    WAITING = 3
    STATUS_CODES = (
        (1, "Confirmed"),
        (0, "Waiting"),
        (-1, "Cancelled"),
    )
    # token_no = models.IntegerField(null=True, blank=True)
    symptoms = models.ManyToManyField(Symptom)
    description = models.TextField(max_length=500, null=True, blank=True)
    appointment_date = models.DateTimeField(
        auto_now_add=True, null=True, blank=True
    )  # year-month-day
    appointment_time = models.TimeField(null=True, blank=True)
    status = models.PositiveSmallIntegerField(
        choices=STATUS_CODES, default=0, null=True, blank=True
    )
    patient_id = models.IntegerField(null=True, blank=True)
    doctor_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return "Appointment ID " + str(self.id)

    @property
    def get_symptoms(self):
        l = []
        for i in self.symptoms.all():
            l.append(i.name)
        return ", ".join(map(str, l))


class AppointmentRecord(models.Model):
    appointment = models.ForeignKey(
        BookAppointment, on_delete=models.CASCADE, null=True, blank=True
    )
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class Notification(models.Model):
    user_id = models.IntegerField(null=True, blank=True)
    message = models.CharField(max_length=1000, null=True, blank=True)
    read = models.BooleanField(default=False, null=True, blank=True)
