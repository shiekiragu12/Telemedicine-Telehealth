from django import forms
from .models import *


class CreateFacility(forms.ModelForm):
    class Meta:
        model = Facility
        fields = ['owner', 'name', 'facility_kind', 'description', 'location', 'city', 'county', 'latitude', 'longitude', 'email',
                  'contact_no', 'address', 'specialities', 'logo', 'cover_image']


class ServiceForm(forms.ModelForm):

    class Meta:
        model = Service
        fields = ['facility', 'doctor', 'name', 'description', 'long_description', 'tags',
                  'category', 'charges', 'image']


class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = ['doctor', 'patient', 'note', 'duration', 'date', 'start_time', 'end_time', 'duration', 'condition',
                  'other_condition', 'consultation_type', 'consultation_category']
