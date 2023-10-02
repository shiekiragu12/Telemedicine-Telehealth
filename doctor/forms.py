from django import forms
from facilities.models import (Qualification, MentalForm, DoctorNote, LabTestRequest, Prescription, Substance,
                               SubstanceUsage)


class QualificationForm(forms.ModelForm):
    class Meta:
        model = Qualification
        fields = ['doctor', 'institution', 'year', 'course', 'file', 'notes']


class MentalHealthForm(forms.ModelForm):
    class Meta:
        model = MentalForm
        fields = ['appointment', 'intervention_terminologies', 'client_behavior', 'practitioner_comment',
                  'services_wanted',
                  'family_counselling_names',
                  'application_date',
                  'language',
                  'send_text_message',
                  'send_whatsapp',
                  'send_email',
                  'emergency_contact_name',
                  'emergency_contact_relationship',
                  'emergency_contact_phone_no',
                  'emergency_contact_email',
                  'referrer_source',
                  'time_lived_in_current_place',
                  'why_seek_counselling',
                  'who_brought_you_into_counselling',
                  'want_counselling_or_someone_else_told_you_to',
                  'counselling_related_topics',
                  'how_many_in_family',
                  'first_born_ro_last_born',
                  'hobbies',
                  'supportive_people',
                  'skills',
                  'family_receiving_counselling_from_us',
                  'who_is_getting_counselling',
                  'ever_been_in_counselling',
                  'counselling_experience',
                  'ever_diagnosed_with_mental_illness',
                  'mental_illness_diagnosed_with',
                  'currently_taking_prescriptions',
                  'prescription_dosage_notes',
                  'currently_having_mental_health_provider',
                  'mental_health_provider_notes',
                  'ever_been_hospitalized',
                  'hospitalized_notes',
                  'ever_attempted_suicide',
                  'suicide_notes',
                  'currently_experiencing_suicidal_thoughts',
                  'access_to_gun',
                  'additional_substance_use_info',
                  'current_health',
                  'aspects_of_health',
                  'selected_slots',
                  'on_site_counselling',
                  'residing_in_cities',
                  'can_be_in_any_of_cities'
                  ]


class SubstanceUsageForm(forms.ModelForm):
    class Meta:
        model = SubstanceUsage
        fields = ['substance', 'age_of_first_use', 'age_of_last_use']


SubstanceUsageFormSet = forms.inlineformset_factory(
    Substance, SubstanceUsage, form=SubstanceUsageForm, extra=10
)


class DoctorNotesForm(forms.ModelForm):
    class Meta:
        model = DoctorNote
        fields = ['facility', 'appointment', 'doctor', 'patient', 'progress_notes', 'treatment_date',
                  'next_treatment_plan', 'attended_treatment']


class LabTestRequestForm(forms.ModelForm):
    class Meta:
        model = LabTestRequest
        fields = ['laboratory', 'appointment', 'urgency', 'sample_date_time', 'fasting', 'sample_type',
                  'other_sample_type', 'drug_therapy', 'other_relevant_clinical_info', 'last_dose',
                  'last_dose_date_time', 'examination_requested', 'additional_tests', 'cervical_cytology',
                  'other_cervical_cytology', 'cervical_cytology_site']


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['facility', 'appointment', 'diagnosis', 'prescription', 'recommendation']
