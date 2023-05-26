from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

from mailer.utils import send_custom_email
from django.conf import settings


# Create your models here.


class County(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    slug = models.SlugField(blank=True)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(County, self).save(*args, **kwargs)


class Constituency(models.Model):
    name = models.CharField(max_length=400, blank=False, null=False)
    slug = models.SlugField(blank=True)
    county = models.ForeignKey(County, blank=True, null=True, on_delete=models.SET_NULL)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Constituency, self).save(*args, **kwargs)


class Condition(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    slug = models.SlugField(blank=True)
    factsheet = models.TextField(blank=True, null=True)
    pathogen = models.TextField(blank=True, null=True)
    clinical_features = models.TextField(blank=True, null=True)
    transmission = models.TextField(blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    treatment = models.TextField(blank=True, null=True)
    prevention = models.TextField(blank=True, null=True)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Condition, self).save(*args, **kwargs)


# Illness is the condition without further information
class Illness(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class FacilitySpeciality(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(FacilitySpeciality, self).save(*args, **kwargs)


class FacilityType(models.Model):
    name = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(FacilityType, self).save(*args, **kwargs)


class Facility(models.Model):
    CHOICES = (
        ('pharmacy', 'Pharmacy'),
        ('nutraceutical', 'Nutraceuticals'),
        ('clinic', 'Clinic'),
        ('hospital', 'Hospital'),
    )
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    # Facility code
    facility_code = models.CharField(max_length=30, null=True, blank=True)

    owner_name = models.TextField(blank=True, null=True)

    facility_type = models.ForeignKey(FacilityType, blank=True, null=True, on_delete=models.SET_NULL)
    facility_kind = models.CharField(max_length=100, blank=True, null=True, choices=CHOICES)    # pharmacy, clinic,
    # nutraceuticals

    name = models.CharField(max_length=200, blank=False, null=False)
    slug = models.SlugField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    location = models.CharField(max_length=100, blank=True, null=False, default="")
    city = models.CharField(max_length=100, blank=True, null=False, default="")

    county = models.ForeignKey(County, on_delete=models.SET_NULL, null=True, blank=False)
    constituency = models.ForeignKey(Constituency, on_delete=models.SET_NULL, null=True, blank=False)

    latitude = models.CharField(max_length=100, blank=False, null=False, default="")
    longitude = models.CharField(max_length=100, blank=False, null=False, default="")

    status = models.BooleanField(default=False)

    email = models.CharField(max_length=100, blank=True, null=False, default="")
    contact_no = models.CharField(max_length=100, blank=True, null=False, default="")
    address = models.CharField(max_length=300, blank=True, null=False, default="")

    shared_prescriptions = models.ManyToManyField('Prescription', blank=True, related_name='shared_encounters')

    specialities = models.ManyToManyField(FacilitySpeciality, blank=True)

    authorized = models.BooleanField(default=False)

    logo = models.FileField(upload_to='facilities/files/logo/', null=True, blank=True)
    cover_image = models.FileField(upload_to='facilities/files/covers/', null=True, blank=True)

    home_page_content = models.TextField(blank=True)
    about_page_content = models.TextField(blank=True)
    online_page_content = models.TextField(blank=True)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


@receiver(post_save, sender=Facility)
def send_new_facility_creation_email(sender, instance, created, **kwargs):
    if created:
        # send_facility_creation_email(instance.refresh_from_db())
        send_custom_email('facility_creation', instance, settings.ADMIN_EMAILS)
        return


class SpecialityField(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    slug = models.SlugField(blank=True, null=True)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(SpecialityField, self).save(*args, **kwargs)


class Doctor(models.Model):
    facilities = models.ManyToManyField(Facility, blank=True)
    user = models.OneToOneField(User, blank=False, null=False, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)

    about = models.TextField()

    license_number = models.CharField(max_length=30, blank=True, null=True)
    regulatory_body = models.CharField(max_length=100, blank=True, null=True)
    license_file = models.FileField(upload_to='providers/files/', blank=False, null=True)

    specialities = models.ManyToManyField(FacilitySpeciality, blank=True)
    speciality_field = models.ForeignKey(SpecialityField, blank=True, null=True, on_delete=models.SET_NULL)

    is_verified = models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


@receiver(post_save, sender=Doctor)
def send_new_doctor_creation_email(sender, instance, created, **kwargs):
    if created:
        send_custom_email('doctor_creation', instance, settings.ADMIN_EMAILS + [instance.user.email])


class QualificationCourse(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    slug = models.SlugField(blank=True, null=True)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(QualificationCourse, self).save(*args, **kwargs)


class Qualification(models.Model):
    doctor = models.ForeignKey(Doctor, blank=True, null=False, on_delete=models.CASCADE, related_name='qualifications')
    course = models.ForeignKey(QualificationCourse, blank=False, null=True, on_delete=models.SET_NULL)
    institution = models.CharField(max_length=100, blank=True, null=False)
    year = models.CharField(max_length=10, blank=True, null=False)
    notes = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='doctors/files/', blank=False, null=True)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.doctor.user.username


class Staff(models.Model):
    facility = models.ForeignKey(Facility, blank=True, null=True, on_delete=models.SET_NULL)
    user = models.OneToOneField(User, blank=False, null=False, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    designation = models.TextField()
    education = models.TextField()

    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Patient(models.Model):
    facility = models.ForeignKey(Facility, blank=True, null=True, on_delete=models.SET_NULL, related_name='patients')
    facilities = models.ManyToManyField(Facility, blank=True, related_name='facilities')
    user = models.OneToOneField(User, blank=False, null=False, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    dob = models.DateField()
    account_sharable = models.BooleanField(default=False)

    reason_for_signup = models.TextField(blank=True, null=True)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


@receiver(post_save, sender=Patient)
def send_new_patient_creation_email(sender, instance, created, **kwargs):
    if created:
        # send_patient_creation_email(instance)
        send_custom_email('patient_creation', instance, settings.ADMIN_EMAILS + [instance.user.email])


class Service(models.Model):
    facility = models.ForeignKey(Facility, blank=True, null=True, on_delete=models.SET_NULL)
    doctor = models.ForeignKey(Doctor, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=False, null=False)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField()
    long_description = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField('mainapp.Tag', blank=True)
    category = models.ForeignKey('ServiceCategory', blank=False, null=False, on_delete=models.CASCADE)
    charges = models.FloatField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    status = models.BooleanField(default=True)
    image = models.ImageField(upload_to="services/images/", blank=False, null=True)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Service, self).save(*args, **kwargs)


class ServiceCategory(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField(blank=True, null=True)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    facility = models.ForeignKey(Facility, blank=True, null=True, on_delete=models.SET_NULL,
                                 related_name="facility_appointments")
    doctor = models.ForeignKey(Doctor, blank=False, null=True, on_delete=models.SET_NULL,
                               related_name="doctor_appointments")
    patient = models.ForeignKey(Patient, blank=False, null=True, on_delete=models.SET_NULL,
                                related_name="patient_appointments")
    note = models.TextField()
    status = models.BooleanField(default=False)
    date = models.DateTimeField()
    start_time = models.CharField(max_length=10, blank=False, null=False, default="")
    end_time = models.CharField(max_length=10, blank=False, null=False, default="")
    condition = models.ForeignKey(Illness, blank=False, null=True, on_delete=models.SET_NULL)
    other_condition = models.CharField(blank=True, null=True, max_length=256)
    consultation_type = models.CharField(max_length=10, blank=False, null=True)
    video_link = models.CharField(max_length=455, blank=True, null=True)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment #-000{self.id}"


@receiver(post_save, sender=Appointment)
def send_new_appointment_creation_email(sender, instance, created, **kwargs):
    if created:
        # send_appointment_creation_email(instance.refresh_from_db())
        send_custom_email('appointment_creation', instance, [instance.doctor.user.email, instance.patient.user.email])


class MedicalFile(models.Model):
    appointment = models.ForeignKey(Appointment, blank=False, null=True, on_delete=models.SET_NULL,
                                    related_name='appointment_medical_files')
    encounter = models.ForeignKey('Encounter', blank=True, null=True, on_delete=models.CASCADE,
                                  related_name='encounter_medical_files')
    file = models.FileField(upload_to='facilities/files/medical/')

    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    updated_on = models.DateTimeField(auto_now_add=True)


class Encounter(models.Model):
    facility = models.ForeignKey(Facility, blank=True, null=True, on_delete=models.SET_NULL)
    doctor = models.ForeignKey(Doctor, blank=False, null=True, on_delete=models.SET_NULL,
                               related_name="doctor_encounters")
    patient = models.ForeignKey(Patient, blank=False, null=True, on_delete=models.SET_NULL,
                                related_name="patient_encounters")
    description = models.TextField()
    date = models.DateTimeField()

    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.patient.user.username


class Prescription(models.Model):
    facility = models.ForeignKey(Facility, blank=True, null=True, on_delete=models.SET_NULL)
    patient = models.ForeignKey('Patient', blank=False, null=True, on_delete=models.SET_NULL,
                                related_name='patient_prescriptions')
    doctor = models.ForeignKey('Doctor', blank=False, null=True, on_delete=models.SET_NULL,
                               related_name='doctor_prescriptions')
    prescription = models.TextField(blank=False)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.user.first_name} {self.patient.user.last_name}"


@receiver(post_save, sender=Prescription)
def send_new_prescription_creation_email(sender, instance, created, **kwargs):
    if created:
        # send_prescription_creation_email(instance.refresh_from_db())
        send_custom_email('prescription_creation', instance, [instance.patient.email])
        return


class SharedPrescription(models.Model):
    facility = models.ForeignKey(Facility, blank=False, null=False, on_delete=models.CASCADE)
    prescription = models.ForeignKey(Prescription, blank=False, null=False, on_delete=models.CASCADE)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.prescription.patient.user.username
