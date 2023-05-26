from django.contrib import admin
from .models import Email, EmailConfiguration, SentEmail
# Register your models here.

admin.site.register(Email)
admin.site.register(EmailConfiguration)
admin.site.register(SentEmail)
