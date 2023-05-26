from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from mailer.utils import send_custom_email


# Create your models here.

class Schedule(models.Model):
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=254, blank=True, unique=True)
    phone = models.IntegerField(blank=True, null=True)
    message = models.CharField(max_length=100, blank=True)
    date = models.DateField(blank=True)

    read = models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)

    def __str__(self):
        return self.name + "'s " + self.name + " schedule"


@receiver(post_save, sender=Schedule)
def send_new_schedule_creation_email(sender, instance, created, **kwargs):
    if created:
        send_custom_email('schedule_creation', instance, [instance.email])


class Analytic(models.Model):
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=254, blank=True, unique=True)
    phone = models.IntegerField(blank=True, null=True)
    message = models.CharField(max_length=100, blank=True)

    read = models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)

    def __str__(self):
        return self.name + "'s " + self.name + " analytic"


@receiver(post_save, sender=Analytic)
def send_new_analytic_creation_email(sender, instance, created, **kwargs):
    if created:
        send_custom_email('analytic_creation', instance, [instance.email])


class Apply(models.Model):
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    patient_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=254, blank=True, unique=True)
    occupation = models.CharField(max_length=100, blank=True)
    phone_number = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    facility_phone_number = models.IntegerField(blank=True, null=True)
    bill = models.IntegerField(blank=True, null=True)
    date_hosipitalized = models.DateField(blank=True, null=True)
    date = models.DateField(blank=True)
    message = models.CharField(max_length=100, blank=True)

    read = models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)

    def __str__(self):
        return self.f_name + "'s " + self.name + " apply"


@receiver(post_save, sender=Apply)
def send_new_apply_creation_email(sender, instance, created, **kwargs):
    if created:
        send_custom_email('apply_creation', instance, [instance.email])


class Equip(models.Model):
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    facility = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=254, blank=True, unique=True)
    phone = models.IntegerField(blank=True, null=True)
    facility_name = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    facility_phone_number = models.IntegerField(blank=True, null=True)
    equip = models.CharField(max_length=100, blank=True)
    message = models.CharField(max_length=100, blank=True)

    read = models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)

    def __str__(self):
        return self.f_name + "'s " + self.f_name + " equip"


@receiver(post_save, sender=Equip)
def send_new_equip_creation_email(sender, instance, created, **kwargs):
    if created:
        send_custom_email('equip_creation', instance, [instance.email])


class Telehealth(models.Model):
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    facility = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=100, blank=True)
    phone = models.IntegerField(blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, unique=True)
    location = models.CharField(max_length=100, blank=True)
    facility_phone_number = models.IntegerField(blank=True, null=True)
    message = models.CharField(max_length=100, blank=True)

    read = models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)

    def __str__(self):
        return self.f_name + "'s " + self.f_name + " telehealth"


@receiver(post_save, sender=Telehealth)
def send_new_telehealth_creation_email(sender, instance, created, **kwargs):
    if created:
        send_custom_email('telehealth_creation', instance, [instance.email])


class DemoRequest(models.Model):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=60, blank=True)
    facility = models.CharField(max_length=100, blank=True)
    requesting_as = models.CharField(max_length=20, blank=False, null=False)
    time = models.TimeField(blank=True, null=True)

    read = models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)

    class Meta:
        verbose_name_plural = 'Demo Requests'

    def __str__(self):
        return f"{self.f_name} {self.l_name}"


@receiver(post_save, sender=DemoRequest)
def send_new_demorequest_creation_email(sender, instance, created, **kwargs):
    if created:
        send_custom_email('demorequest_creation', instance, [instance.email])


class TypeFacility(models.Model):
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name + "'s " + self.name + " typefacility"


class Book(models.Model):
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    message = models.CharField(max_length=100, blank=True)

    read = models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)

    def __str__(self):
        return self.f_name + "'s " + self.f_name + " book"


@receiver(post_save, sender=Book)
def send_new_book_creation_email(sender, instance, created, **kwargs):
    if created:
        send_custom_email('book_creation', instance, [instance.email])


class Firstaid(models.Model):
    org_name = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    role = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    core = models.TextField(max_length=100, blank=True)
    no_of_employees = models.CharField(max_length=100, blank=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)

    read = models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)

    def __str__(self):
        return self.org_name + "'s " + self.f_name + " firstaid"


@receiver(post_save, sender=Firstaid)
def send_new_firstaid_creation_email(sender, instance, created, **kwargs):
    if created:
        send_custom_email('firstaid_creation', instance, [instance.email])
