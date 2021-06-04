from django.db import models
from django.contrib.auth.models import User
from hospital.models import Hospital
from home.models import Departments

# Create your models here.
class Degree(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)
    hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, null=True, blank=True
    )
    clinic = models.CharField(
        max_length=100, null=True, blank=True
    )  # if hospital is Null , then clinic jrur hoga, apply validation
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, null=True, blank=True
    )
    degree = models.ManyToManyField(Degree)
    fees = models.IntegerField(null=True, blank=True)
    mobile = models.CharField(max_length=20, null=False)
    date_of_birth = models.DateField(null=True, blank=True)  # m/d/y
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    rating = models.IntegerField(default=0)
    cnt = models.IntegerField(default=0)
    """
    profile_pic= models.ImageField(upload_to='profile_pic/DoctorProfilePic/',null=True,blank=True)
    """

    def __str__(self):
        return self.user.get_full_name()

    @property
    def get_rating(self):
        if self.cnt == 0:
            return 0
        return self.rating / self.cnt

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id
