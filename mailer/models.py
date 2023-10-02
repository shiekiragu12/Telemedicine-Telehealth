from django.contrib.auth.models import User
from django.db import models


class Email(models.Model):

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='email_created_by')
    subject = models.CharField(max_length=200)
    description = models.TextField()
    body = models.TextField()
    color = models.CharField(max_length=30, blank=True, null=True)

    identifier = models.CharField(max_length=30, blank=True, null=True, default="")
    created_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class EmailConfiguration(models.Model):

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    email = models.CharField(max_length=100, blank=False, null=False, default="")
    host = models.CharField(max_length=100, blank=False, null=False, default="")
    port = models.CharField(max_length=100, blank=False, null=False, default="")
    use_tls = models.BooleanField(default=True)
    password = models.CharField(max_length=100, blank=False, null=False, default="")
    color = models.CharField(max_length=30, blank=True, null=True)
    created_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.email} - {self.title}"


class SentEmail(models.Model):
    receiver = models.EmailField(blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField()
    sent = models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.receiver}"

