from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['country_code', 'phone_number', 'gender', 'address', 'country',
                  'city', 'dob', 'salutation', 'pronouns', 'race', 'sexual_orientation',
                  'preferred_name']
