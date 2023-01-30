from django import forms
from .models import *


class CreateFacility(forms.ModelForm):
    class Meta:
        model = Facility
        fields = ['owner', 'name', 'description', 'location', 'city', 'county', 'latitude', 'longitude', 'email',
                  'contact_no', 'address', 'specialities', 'logo', 'cover_image']
