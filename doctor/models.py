from django.db import models
from django.contrib.auth.models import User
from home.models import Departments, Symptom
from patient.models import Patient

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
    PATIENT = 1
    DOCTOR = 2
    ADMIN = 3
    ROLE_CHOICES = (
        (PATIENT, "Patient"),
        (DOCTOR, "Doctor"),
        (ADMIN, "Admin"),
    )
    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES, default=DOCTOR, null=True, blank=True
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)
    # appointments = models.ForeignKey(BookAppointment, null=True, blank=True)
    clinic = models.CharField(
        max_length=100, null=True, blank=True
    )  # if hospital is Null , then clinic jrur hoga, apply validation
    open_time = models.TimeField(
        default="09:00", help_text="09:00", null=True, blank=True
    )
    close_time = models.TimeField(
        default="15:00", help_text="09:00", null=True, blank=True
    )
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, null=True, blank=True
    )
    degree = models.ManyToManyField(Degree)
    fees = models.IntegerField(default=100, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=False)
    date_of_birth = models.DateField(default="07/16/1997", null=True, blank=True)
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
    def get_id(self):
        return self.user.id

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_role(self):
        return self.role

    @property
    def get_rating(self):
        if self.cnt == 0:
            return 0
        return self.rating / self.cnt

    @property
    def get_degree(self):
        return self.degree.all()

    @property
    def get_fees(self):
        return self.fees

    @property
    def get_department(self):
        return self.department

    @property
    def get_hospital(self):
        return self.hospital

    @property
    def get_clinic(self):
        return self.clinic

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
        return ",".join(map(str, l))

    @property
    def get_clinic_open_close_time(self):
        return self.open_time, self.close_time

    @property
    def get_degree(self):
        l = []
        for i in self.degree.all():
            l.append(i.name)
        return ", ".join(map(str, l))


class BookAppointment(models.Model):
    CONFIRMED = 1
    CANCELLED = -1
    WAITING = 0
    STATUS_CODES = (
        (1, "Confirmed"),
        (0, "Waiting"),
        (-1, "Cancelled"),
    )
    # token_no = models.IntegerField(null=True, blank=True)
    symptoms = models.ManyToManyField(Symptom)
    description = models.TextField(max_length=500, null=True, blank=True)
    appointment_date = models.DateField(
        auto_now_add=True, null=True, blank=True
    )  # year-month-day
    appointment_time = models.TimeField(null=True, blank=True)
    status = models.PositiveSmallIntegerField(
        choices=STATUS_CODES, default=0, null=True, blank=True
    )
    patient_id = models.IntegerField(null=True, blank=True)
    doctor_id = models.IntegerField(null=True, blank=True)
    fees_submitted = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return "Appointment ID " + str(self.id)

    @property
    def is_appt_approved(self):
        if self.status == 1:
            return 1
        return 0

    @property
    def get_symptoms(self):
        l = []
        for i in self.symptoms.all():
            l.append(i.name)
        return ", ".join(map(str, l))

    @property
    def get_doctor(self):
        return Doctor.objects.get(id=self.doctor_id)

    @property
    def get_patient(self):
        return Patient.objects.get(id=self.patient_id)

    @property
    def get_patient_mobile(self):
        patient = Patient.objects.get(id=self.patient_id)
        if patient.mobile:
            return patient.mobile
        return "NA"

    @property
    def get_patient_address(self):
        patient = Patient.objects.get(id=self.patient_id)
        l = []
        if patient.address:
            l.append(patient.address)
        if patient.city:
            l.append(patient.city)
        if patient.state:
            l.append(patient.state)
        if l == []:
            return "NA"
        return " ".join(map(str, l))

    @property
    def get_fees_status(self):
        if self.fees_submitted == 0:
            return "No"
        return "Yes"


class Review(models.Model):
    CHOICES = (("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"))
    doctor_id = models.IntegerField(null=True, blank=True)
    patient_id = models.IntegerField(null=True, blank=True)
    rating = models.CharField(max_length=1, choices=CHOICES, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    @property
    def get_patient(self):
        return Patient.objects.get(id=self.patient_id)

    @property
    def get_doctor(self):
        return Doctor.objects.get(id=self.doctor_id)
