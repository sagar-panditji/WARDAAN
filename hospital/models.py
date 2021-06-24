from django.db import models
from django.contrib.auth.models import User
from home.models import Departments

# Create your models here.


class Hospital(models.Model):
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
        choices=ROLE_CHOICES, default=HOSPITAL, null=True, blank=True
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    departments = models.ManyToManyField(Departments)
    mobile = models.CharField(max_length=20, null=False)
    start_date = models.DateField(auto_now=True, null=True, blank=True)  # m/d/y
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    no_of_beds = models.IntegerField(null=True, blank=True)
    rating = models.IntegerField(default=0)
    cnt = models.IntegerField(default=0)
    icu_fees = models.IntegerField(default=1000)
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

    @property
    def get_role(self):
        return self.role

    @property
    def get_departments(self):
        l = []
        for i in self.departments.all():
            l.append(i.name)
        return ", ".join(map(str, l))

    @property
    def count_departments(self):
        cnt = 0
        for i in self.departments.all():
            cnt += 1
        return cnt
