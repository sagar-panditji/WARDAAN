from django.db import models
from django.contrib.auth.models import User
from home.models import Departments

# Create your models here.


class Hospital(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    department = models.ManyToManyField(Departments)
    mobile = models.CharField(max_length=20, null=False)
    start_date = models.DateField(auto_now=True, null=True, blank=True)  # m/d/y
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    no_of_beds = models.IntegerField(null=True, blank=True)
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
