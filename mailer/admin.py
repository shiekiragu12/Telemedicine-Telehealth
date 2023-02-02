from django.contrib import admin
from .models import Email, EmailConfiguration
# Register your models here.

admin.site.register(Email)
admin.site.register(EmailConfiguration)
