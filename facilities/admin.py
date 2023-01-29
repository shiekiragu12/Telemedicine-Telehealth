from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register([Disease,FacilitySpeciality,Facility,Doctor,Qualification,Reception,Patient,Service,ServiceCategory,Appointment,MedicalFile,Encounter])

