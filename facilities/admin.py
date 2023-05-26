from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register([County, Constituency])
# Illness is the condition without further information
admin.site.register([Condition, Illness])
admin.site.register([FacilitySpeciality])
admin.site.register(Facility)
admin.site.register(Doctor)
admin.site.register(Qualification)
admin.site.register(Staff)
admin.site.register(Patient)
admin.site.register(Service)
admin.site.register(ServiceCategory)
admin.site.register(Appointment)
admin.site.register(MedicalFile)
admin.site.register([Encounter, Prescription])
admin.site.register([QualificationCourse, SpecialityField])
