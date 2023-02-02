from django.contrib.auth.models import User
from django.db import models


class Email(models.Model):

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='email_created_by')
    subject = models.CharField(max_length=200)
    description = models.TextField()
    body = models.TextField()
    color = models.CharField(max_length=30)

    identifier = models.CharField(max_length=30, blank=False, null=False, default="")
    created_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class EmailConfiguration(models.Model):

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    email = models.TextField()
    host = models.TextField()
    port = models.IntegerField()
    use_tls = models.BooleanField(default=True)
    password = models.TextField()
    color = models.CharField(max_length=30)
    created_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.email} - {self.title}"
