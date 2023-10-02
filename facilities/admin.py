from django.contrib import admin
from .models import *

# Register your models here.
admin.site.site_title = 'Your Custom Site Title'
admin.site.index_title = 'Your Custom Index Title'


class DoctorAdmin(admin.ModelAdmin):
    list_display = ['doctor_name', 'is_verified', 'display_on_homepage', 'display_on_mental_health']
    list_filter = ['is_verified', 'display_on_homepage', 'display_on_mental_health', 'speciality_field']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__email']
    list_editable = ['is_verified', 'display_on_homepage', 'display_on_mental_health']

    @staticmethod
    def doctor_name(instance):
        return instance.user.get_full_name()


class AppointmentTimeAdmin(admin.ModelAdmin):
    list_display = ['id', 'time', 'order', 'active']
    list_editable = ['time', 'order', 'active']


class AppointmentDurationAdmin(admin.ModelAdmin):
    list_display = ['id', 'minutes', 'order', 'active']
    list_editable = ['minutes', 'order', 'active']


class ExaminationRequestedInline(admin.TabularInline):
    model = ExaminationRequested
    # fields = ['name']


class ExaminationRequestedGroupAdmin(admin.ModelAdmin):
    inlines = [ExaminationRequestedInline]


class SubstanceUserTitleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'form_name', 'type', 'placeholder']
    list_editable = ['title', 'form_name', 'type', 'placeholder']


admin.site.register([County, Constituency])
# Illness is the condition without extra information
admin.site.register([Condition, Illness])
admin.site.register([Speciality])
admin.site.register(Facility)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Qualification)
admin.site.register(Staff)
admin.site.register(Patient)
admin.site.register(Service)
admin.site.register(ServiceCategory)
admin.site.register(Appointment)
admin.site.register(MedicalFile)
admin.site.register([DoctorNote, Prescription, MentalForm])
admin.site.register([QualificationCourse, ProviderCategory])
admin.site.register(AppointmentTime, AppointmentTimeAdmin)
admin.site.register(AppointmentDuration, AppointmentDurationAdmin)
admin.site.register(
    [SampleType, ExaminationRequested, CervicalCytologySite, CervicalCytology,
     LabTestRequest])
admin.site.register(ExaminationRequestedGroup, ExaminationRequestedGroupAdmin)
admin.site.register([InterventionTerminology, ClientBehavior])
admin.site.register([YesNo, DayAvailability, TimeAvailability])
admin.site.register([CounsellingTopic, CounsellingExperience])
admin.site.register([Substance, SubstanceUsage, TeletherapyService])
admin.site.register(SubstanceUseTitle, SubstanceUserTitleAdmin)

