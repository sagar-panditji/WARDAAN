from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Patient(models.Model):
    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    )
    PATIENT = 1
    DOCTOR = 2
    HOSPITAL = 3
    ADMIN = 4
    ROLE_CHOICES = (
        (PATIENT, "Patient"),
        (DOCTOR, "Doctor"),
        (HOSPITAL, "Hospital"),
        (ADMIN, "Admin"),
    )
    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES, default=PATIENT, null=True, blank=True
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, null=True, blank=True
    )
    mobile = models.CharField(max_length=20, null=False)
    date_of_birth = models.DateField(null=True, blank=True)  # m/d/y
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True
    )

    def __str__(self):
        return self.user.get_full_name()

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    @property
    def get_role(self):
        return self.role

    @property
    def get_address(self):
        l = []
        if self.address:
            l.append(self.address)
        if self.city:
            l.append(self.city)
        if self.state:
            l.append(self.state)
        if l == []:
            return "NA"
        return ", ".join(map(str, l))
