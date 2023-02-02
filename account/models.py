from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    gender = models.CharField(max_length=30, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(max_length=30, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profile/photos/')
    dob = models.DateField(blank=True, null=True)

    created = models.DateTimeField(auto_now=True, auto_created=True)
    updated = models.DateTimeField(auto_now_add=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
            instance.profile.save()

        post_save.connect(Profile, sender=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        Profile.objects.get_or_create(user=instance)
        instance.profile.save()
