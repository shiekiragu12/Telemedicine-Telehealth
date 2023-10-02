from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

from mailer.utils import send_custom_email
from django.conf import settings
from website.models import Notification
from django.shortcuts import reverse


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


class Speciality(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Speciality, self).save(*args, **kwargs)


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
    facility_kind = models.CharField(max_length=100, blank=True, null=True, choices=CHOICES)  # pharmacy, clinic,
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

    specialities = models.ManyToManyField(Speciality, blank=True)

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
        send_custom_email('facility_creation', instance, settings.ADMIN_EMAILS)
        Notification.objects.create(to_admin=True, title="New facility created",
                                    message=f"A new facility has been created. Check it out "
                                            f"<a href='{reverse('super-admin-facilities-single', instance.id)}'>"
                                            f"here</a>")
        return


class ProviderCategory(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    slug = models.SlugField(blank=True, null=True)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(ProviderCategory, self).save(*args, **kwargs)


class Doctor(models.Model):
    facilities = models.ManyToManyField(Facility, blank=True)
    user = models.OneToOneField(User, blank=False, null=False, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)

    about = models.TextField()

    license_number = models.CharField(max_length=30, blank=True, null=True)
    regulatory_body = models.CharField(max_length=100, blank=True, null=True)
    license_file = models.FileField(upload_to='providers/files/', blank=False, null=True)

    specialities = models.ManyToManyField(Speciality, blank=True)
    speciality_field = models.ForeignKey(ProviderCategory, blank=True, null=True, on_delete=models.SET_NULL)

    is_verified = models.BooleanField(default=False)
    display_on_homepage = models.BooleanField(default=False)
    display_on_mental_health = models.BooleanField(default=False)

    name = models.CharField(blank=True, null=True, max_length=50)
    has_read_terms = models.BooleanField(default=False)
    has_signed_contract = models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"


@receiver(post_save, sender=Doctor)
def send_new_doctor_creation_email(sender, instance, created, **kwargs):
    if created:
        send_custom_email('doctor_creation', instance, settings.ADMIN_EMAILS + [instance.user.email])
        Notification.objects.create(to_admin=True, title="New doctor created",
                                    message=f"A new doctor has been created. Check it out "
                                            f"<a href='{reverse('super-admin-doctors-single', instance.id)}'>"
                                            f"here</a>")
        return


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
    institution = models.CharField(max_length=100, blank=False, null=False)
    year = models.CharField(max_length=10, blank=False, null=False)
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
        send_custom_email('patient_creation', instance, settings.ADMIN_EMAILS + [instance.user.email])
        Notification.objects.create(to_admin=True, title="New patient created",
                                    message=f"A new patient has been created. Check it out "
                                            f"<a href='{reverse('super-admin-patients-single', instance.id)}'>"
                                            f"here</a>")
        return


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


class AppointmentTime(models.Model):
    # 9:30 AM
    time = models.TimeField(unique=True)
    active = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.time.__str__()


class AppointmentDuration(models.Model):
    # 10
    minutes = models.IntegerField(unique=True)
    active = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.minutes.__str__()


class Appointment(models.Model):
    CONSULTATION_CATEGORY_CHOICES = (
        ('mental', 'Mental'),
        ('medical', 'Medical')
    )

    facility = models.ForeignKey(Facility, blank=True, null=True, on_delete=models.SET_NULL,
                                 related_name="facility_appointments")
    doctor = models.ForeignKey(Doctor, blank=False, null=True, on_delete=models.SET_NULL,
                               related_name="doctor_appointments")
    patient = models.ForeignKey(Patient, blank=False, null=True, on_delete=models.SET_NULL,
                                related_name="patient_appointments")
    note = models.TextField()
    status = models.BooleanField(default=False)

    date = models.DateField(blank=False, null=True)
    start_time = models.ForeignKey(AppointmentTime, blank=False, null=True, default="", on_delete=models.SET_NULL)
    duration = models.ForeignKey(AppointmentDuration, blank=False, null=True, on_delete=models.SET_NULL)
    end_time = models.TimeField(blank=True, null=True)

    condition = models.ForeignKey(Illness, blank=False, null=True, on_delete=models.SET_NULL)
    other_condition = models.CharField(blank=True, null=True, max_length=256)

    consultation_type = models.CharField(max_length=10, blank=False, null=True)
    consultation_category = models.CharField(max_length=50, blank=False, null=True,
                                             choices=CONSULTATION_CATEGORY_CHOICES)

    video_link = models.CharField(max_length=455, blank=True, null=True)
    zoom_meeting_creation_response = models.TextField(blank=True, null=True)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment:--{self.id}"


@receiver(post_save, sender=Appointment)
def send_new_appointment_creation_email(sender, instance, created, **kwargs):
    if created:
        send_custom_email('appointment_creation', instance, [instance.doctor.user.email])
        send_custom_email('patient_appointment_creation', instance, [instance.patient.user.email])
        Notification(from_user=instance.patient, to_user=instance.doctor, title="New appointment", message=f"Patient "
                                                                                                           f"{instance.patient.user.get_full_name()}"
                                                                                                           f"Has created a new appointment with your. Check it out"
                                                                                                           f"<a href='{reverse('doctor:single-appointment', instance.id)}'>here</a>")


class MedicalFile(models.Model):
    appointment = models.ForeignKey(Appointment, blank=False, null=True, on_delete=models.SET_NULL,
                                    related_name='appointment_medical_files')
    encounter = models.ForeignKey('DoctorNote', blank=True, null=True, on_delete=models.CASCADE,
                                  related_name='encounter_medical_files')
    file = models.FileField(upload_to='facilities/files/medical/')

    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    updated_on = models.DateTimeField(auto_now_add=True)


class DoctorNote(models.Model):
    facility = models.ForeignKey(Facility, blank=True, null=True, on_delete=models.SET_NULL)
    appointment = models.ForeignKey(Appointment, blank=True, null=True, on_delete=models.SET_NULL)
    doctor = models.ForeignKey(Doctor, blank=False, null=True, on_delete=models.SET_NULL,
                               related_name="doctor_encounters")
    patient = models.ForeignKey(Patient, blank=False, null=True, on_delete=models.SET_NULL,
                                related_name="patient_encounters")
    progress_notes = models.TextField(blank=False, null=True)
    treatment_date = models.DateTimeField(blank=False, null=True)
    next_treatment_plan = models.TextField(blank=True, null=True)
    attended_treatment = models.BooleanField(blank=True, null=True)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.patient.user.username


class Prescription(models.Model):
    facility = models.ForeignKey(Facility, blank=True, null=True, on_delete=models.SET_NULL)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, blank=False, null=True)

    diagnosis = models.TextField(blank=False, null=True)
    prescription = models.TextField(blank=False, null=True)
    recommendation = models.TextField(blank=False, null=True)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f"{self.patient.user.first_name} {self.patient.user.last_name}"


@receiver(post_save, sender=Prescription)
def send_new_prescription_creation_email(sender, instance, created, **kwargs):
    if created:
        send_custom_email('prescription_creation', instance, [instance.patient.email])
        Notification(from_user=instance.appointment.doctor.user, to_user=instance.appointment.patient.user,
                     title="New prescription", message=f"Doctor "
                                                       f"{instance.appointment.doctor.user.get_full_name()}"
                                                       f"Has created a new prescription for you. Check it out"
                                                       f"<a href='#'>here</a>")


class SharedPrescription(models.Model):
    facility = models.ForeignKey(Facility, blank=False, null=False, on_delete=models.CASCADE)
    prescription = models.ForeignKey(Prescription, blank=False, null=False, on_delete=models.CASCADE)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return


class SampleType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class ExaminationRequestedGroup(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class ExaminationRequested(models.Model):
    group = models.ForeignKey(ExaminationRequestedGroup, blank=False, null=True, on_delete=models.CASCADE,
                              related_name='examinations_requested')
    name = models.CharField(max_length=30)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    updated_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class CervicalCytology(models.Model):
    name = models.CharField(max_length=30)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    updated_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class CervicalCytologySite(models.Model):
    name = models.CharField(max_length=30)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    updated_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class LabTestRequest(models.Model):
    laboratory = models.ForeignKey(Facility, blank=False, null=True, on_delete=models.SET_NULL)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, blank=False, null=True)

    urgency = models.CharField(choices=[('Normal', 'Normal'), ('Urgent', 'Urgent')], max_length=10,
                               blank=False, null=True)
    # Sample details
    sample_date_time = models.DateTimeField(blank=True, null=True)
    fasting = models.BooleanField(blank=True, null=True)
    sample_type = models.ManyToManyField(SampleType, blank=True)
    other_sample_type = models.CharField(max_length=50, blank=True, null=True)

    # Relevant clinical information
    drug_therapy = models.TextField(blank=True, null=True)
    other_relevant_clinical_info = models.TextField(blank=True, null=True)
    last_dose = models.TextField(blank=True, null=True)
    last_dose_date_time = models.DateTimeField(blank=True, null=True)

    examination_requested = models.ManyToManyField(ExaminationRequested, blank=True)
    additional_tests = models.TextField(blank=True, null=True)

    cervical_cytology = models.ManyToManyField(CervicalCytology, blank=True)
    other_cervical_cytology = models.CharField(max_length=50, blank=True, null=True)
    cervical_cytology_site = models.ManyToManyField(CervicalCytologySite, blank=True)

    requester_signature = models.CharField(max_length=100)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    updated_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return (f"Lab Test Request for "
                f"{self.appointment.patient.user.get_full_name()} by {self.appointment.doctor.user.get_full_name()}")


@receiver(post_save, sender=LabTestRequest)
def lab_test_form_creation(sender, instance, created, **kwargs):
    if created:
        Notification(from_user=instance.appointment.doctor.user, facility_id={instance.laboratory.id},
                     title="New lab test request",
                     message=f"Doctor "
                             f"{instance.appointment.doctor.user.get_full_name()}"
                             f"Has requested for a lab test.<br> Urgency: {instance.urgency}"
                             f"<a href='#'>View</a>")


class InterventionTerminology(models.Model):
    name = models.CharField(max_length=30)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    updated_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class ClientBehavior(models.Model):
    name = models.CharField(max_length=30)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    updated_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class CounsellingTopic(models.Model):
    name = models.CharField(max_length=30)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    updated_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class CounsellingExperience(models.Model):
    name = models.CharField(max_length=30)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    updated_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class SubstanceUseTitle(models.Model):
    title = models.CharField(max_length=200, unique=True)
    form_name = models.CharField(max_length=200, unique=True, blank=False, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    placeholder = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.title


class Substance(models.Model):
    title = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.title


class SubstanceUsage(models.Model):
    mental_form = models.ForeignKey('MentalForm', on_delete=models.CASCADE, related_name='substance_usage', null=True)
    substance = models.ForeignKey(Substance, on_delete=models.CASCADE, null=True)
    method_of_use = models.CharField(max_length=40, blank=True, null=True)
    amount_typically_used = models.CharField(max_length=40, blank=True, null=True)
    age_of_first_use = models.IntegerField(blank=True, null=True)
    age_of_last_use = models.IntegerField(blank=True, null=True)
    used_in_last_48_hrs = models.CharField(max_length=10, blank=True, null=True)
    used_in_last_30_days = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.substance.title if self.substance else 'No Substance'


class DayAvailability(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    day = models.CharField(max_length=20, choices=DAY_CHOICES)

    def __str__(self):
        return self.day


class TimeAvailability(models.Model):
    TIME_CHOICES = [
        ('Morning', 'Morning'),
        ('Afternoon', 'Afternoon'),
        ('Evening', 'Evening'),
    ]

    time_slot = models.CharField(max_length=20, choices=TIME_CHOICES)

    def __str__(self):
        return self.time_slot


class YesNo(models.Model):
    title = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.title


class TeletherapyService(models.Model):
    title = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.title


class MentalForm(models.Model):
    appointment = models.ForeignKey(Appointment, blank=False, null=True, on_delete=models.CASCADE)

    services_wanted = models.ForeignKey(TeletherapyService, blank=True, null=True, on_delete=models.SET_NULL)
    family_counselling_names = models.TextField(blank=True, null=True)
    application_date = models.DateField(blank=True, null=True)

    language = models.CharField(max_length=50, blank=True, null=True)
    send_text_message = models.CharField(max_length=10, blank=True, null=True)
    send_whatsapp = models.CharField(max_length=10, blank=True, null=True)
    send_email = models.CharField(max_length=10, blank=True, null=True)

    # Patient data
    emergency_contact_name = models.CharField(max_length=80, blank=True, null=True)
    emergency_contact_relationship = models.CharField(max_length=80, blank=True, null=True)
    emergency_contact_phone_no = models.CharField(max_length=80, blank=True, null=True)
    emergency_contact_email = models.CharField(max_length=80, blank=True, null=True)

    referrer_source = models.CharField(max_length=80, blank=True, null=True)
    time_lived_in_current_place = models.CharField(max_length=80, blank=True, null=True)

    why_seek_counselling = models.TextField(blank=True, null=True)
    who_brought_you_into_counselling = models.CharField(max_length=80, blank=True, null=True)

    want_counselling_or_someone_else_told_you_to = models.CharField(max_length=80, blank=True, null=True)
    counselling_related_topics = models.ManyToManyField(CounsellingTopic, blank=True)

    how_many_in_family = models.CharField(max_length=80, blank=True, null=True)
    first_born_ro_last_born = models.CharField(max_length=80, blank=True, null=True)

    hobbies = models.TextField(blank=True, null=True)
    supportive_people = models.CharField(max_length=300, blank=True, null=True)
    skills = models.TextField(blank=True, null=True)

    family_receiving_counselling_from_us = models.CharField(max_length=10, blank=True, null=True)
    who_is_getting_counselling = models.CharField(max_length=300, blank=True, null=True)

    ever_been_in_counselling = models.CharField(max_length=300, blank=True, null=True)
    counselling_experience = models.ManyToManyField(CounsellingExperience, blank=True)

    ever_diagnosed_with_mental_illness = models.CharField(max_length=10, blank=True, null=True)
    mental_illness_diagnosed_with = models.TextField(blank=True, null=True)

    currently_taking_prescriptions = models.CharField(max_length=10, blank=True, null=True)
    prescription_dosage_notes = models.TextField(blank=True, null=True)

    currently_having_mental_health_provider = models.CharField(max_length=10, blank=True, null=True)
    mental_health_provider_notes = models.TextField(blank=True, null=True)

    ever_been_hospitalized = models.CharField(max_length=10, blank=True, null=True)
    hospitalized_notes = models.TextField(blank=True, null=True)

    ever_attempted_suicide = models.CharField(max_length=10, blank=True, null=True)
    suicide_notes = models.TextField(blank=True, null=True)

    currently_experiencing_suicidal_thoughts = models.CharField(max_length=10, blank=True, null=True)
    access_to_gun = models.CharField(max_length=10, blank=True, null=True)

    additional_substance_use_info = models.TextField(blank=True, null=True)
    current_health = models.TextField(blank=True, null=True)
    aspects_of_health = models.TextField(blank=True, null=True)

    selected_slots = models.TextField(blank=True, null=True)
    on_site_counselling = models.TextField(blank=True, null=True)

    # Medical provider data
    intervention_terminologies = models.ManyToManyField(InterventionTerminology, blank=True)
    client_behavior = models.ManyToManyField(ClientBehavior, blank=True)
    practitioner_comment = models.TextField(blank=True, null=True)

    residing_in_cities = models.CharField(max_length=10, blank=True, null=True)
    can_be_in_any_of_cities = models.CharField(max_length=10, blank=True, null=True)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    updated_on = models.DateTimeField(auto_now_add=True, null=True)
