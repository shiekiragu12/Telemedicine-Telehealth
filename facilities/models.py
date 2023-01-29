from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Disease(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField()

    created = models.DateTimeField(auto_now=True, auto_created=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class FacilitySpeciality(models.Model):
    name = models.CharField(max_length=100)

    created = models.DateTimeField(auto_now=True, auto_created=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Facility(models.Model):
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField()
    location = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    email = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=100)
    specialities = models.ManyToManyField(FacilitySpeciality, blank=True)

    created = models.DateTimeField(auto_now=True, auto_created=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    facility = models.ForeignKey(Facility, blank=True, null=True, on_delete=models.SET_NULL)
    user = models.OneToOneField(User, blank=False, null=False, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    description = models.TextField()

    created = models.DateTimeField(auto_now=True, auto_created=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Qualification(models.Model):
    doctor = models.ForeignKey(Doctor, blank=True, null=False, on_delete=models.CASCADE)
    degree = models.CharField(max_length=10, blank=False, null=False)
    university = models.CharField(max_length=10, blank=False, null=False)
    year = models.CharField(max_length=10, blank=False, null=False)

    created = models.DateTimeField(auto_now=True, auto_created=True)
    updated = models.DateTimeField(auto_now_add=True)


class Reception(models.Model):
    facility = models.ForeignKey(Facility, blank=True, null=True, on_delete=models.SET_NULL)
    user = models.OneToOneField(User, blank=False, null=False, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now=True, auto_created=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Patient(models.Model):
    facility = models.ForeignKey(Facility, blank=True, null=True, on_delete=models.SET_NULL)
    user = models.OneToOneField(User, blank=False, null=False, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=5)
    dob = models.DateField()

    created = models.DateTimeField(auto_now=True, auto_created=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Service(models.Model):
    facility = models.ForeignKey(Facility, blank=True, null=True, on_delete=models.SET_NULL)
    doctor = models.ForeignKey(Doctor, blank=False, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField()
    category = models.ForeignKey('ServiceCategory', blank=False, null=False, on_delete=models.CASCADE)
    charges = models.FloatField()
    duration = models.IntegerField()
    status = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now=True, auto_created=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ServiceCategory(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField()

    created = models.DateTimeField(auto_now=True, auto_created=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    facility = models.ForeignKey(Facility, blank=True, null=True, on_delete=models.SET_NULL)
    doctor = models.ForeignKey(Doctor, blank=False, null=True, on_delete=models.SET_NULL)
    patient = models.ForeignKey(Patient, blank=False, null=True, on_delete=models.SET_NULL)
    description = models.TextField()
    status = models.BooleanField()
    available_slot = models.DateTimeField()

    created = models.DateTimeField(auto_now=True, auto_created=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.patient.user.username


class MedicalFile(models.Model):
    appointment = models.ForeignKey(Appointment, blank=False, null=True, on_delete=models.SET_NULL)
    file = models.FileField(upload_to='medical/files/')

    created = models.DateTimeField(auto_now=True, auto_created=True)
    updated = models.DateTimeField(auto_now_add=True)


class Encounter(models.Model):
    facility = models.ForeignKey(Facility, blank=True, null=True, on_delete=models.SET_NULL)
    doctor = models.ForeignKey(Doctor, blank=False, null=True, on_delete=models.SET_NULL)
    patient = models.ForeignKey(Patient, blank=False, null=True, on_delete=models.SET_NULL)
    description = models.TextField()
    date = models.DateTimeField()

    created = models.DateTimeField(auto_now=True, auto_created=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.patient.user.username
