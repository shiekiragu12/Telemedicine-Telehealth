from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from mailer.moreviews import send_account_creation_email
from mailer.utils import send_custom_email


# Create your models here.

# This method listens on user model, one an account is created, it sends an email
@receiver(post_save, sender=User)
def send_new_account_creation_email(sender, instance, created, **kwargs):
    if created:
        # send_account_creation_email(instance)
        send_custom_email('account_creation', instance, [instance.email])


class Profile(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    country_code = models.CharField(max_length=10, blank=True, null=True)
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    gender = models.CharField(max_length=30, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profile/photos/')
    dob = models.DateField(blank=True, null=True)

    created = models.DateTimeField(auto_now=True, auto_created=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Profile.objects.create(user=instance)
    #         instance.profile.save()
    #
    #     post_save.connect(Profile, sender=instance)
    #
    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     Profile.objects.get_or_create(user=instance)
    #     instance.profile.save()
