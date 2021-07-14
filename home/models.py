from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Symptom(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


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
    symptoms = models.ManyToManyField(Symptom)
    url = models.URLField(
        max_length=250,
        default="https://www.imsanz.org.au/about-us/what-is-a-general-physician",
    )

    def __str__(self):
        return self.name

    @property
    def get_symptoms(self):
        l = []
        for i in self.symptoms.all():
            l.append(i)
        return ", ".join(map(str, l))


class Disease(models.Model):
    name = models.CharField(max_length=100)
    symptoms = models.ManyToManyField(Symptom)

    def __str__(self):
        return self.name


class Notification(models.Model):
    user_id = models.IntegerField(null=True, blank=True)
    message = models.CharField(max_length=1000, null=True, blank=True)
    read = models.BooleanField(default=False, null=True, blank=True)


class PaymentOrder(models.Model):
    doctor_id = models.IntegerField(null=True, blank=True)
    patient_id = models.IntegerField(null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)
