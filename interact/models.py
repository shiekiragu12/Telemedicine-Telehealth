from django.db import models
from django.contrib.auth.models import User

from facilities.models import Appointment


# Create your models here.


class ChatFile(models.Model):
    file = models.FileField(upload_to="user-chats/files/", blank=False, null=False)
    file_type = models.CharField(max_length=5, blank=True, null=True)


class ChatMessage(models.Model):
    appointment = models.ForeignKey(Appointment, blank=False, null=True, on_delete=models.SET_NULL,
                                    help_text="Appointment")
    sender = models.ForeignKey(User, blank=False, null=True, on_delete=models.SET_NULL)
    text = models.TextField(blank=False, null=False)
    files = models.ManyToManyField(ChatFile, blank=True)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)
