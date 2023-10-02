from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from .models import *
from account.publicserializers import PubUserSerializer


class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = County
        fields = '__all__'


class ConstituencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Constituency
        fields = '__all__'


class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = '__all__'


class IllnessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Illness
        fields = '__all__'


class SpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Speciality
        fields = '__all__'


class FacilityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityType
        fields = '__all__'


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ['id', 'owner', 'owner_name', 'facility_type', 'facility_code', 'facility_kind', 'name', 'slug', 'description', 'location',
                  'city', 'county',
                  'constituency', 'latitude', 'longitude', 'status', 'email', 'contact_no', 'address', 'specialities',
                  'authorized', 'logo', 'cover_image', 'home_page_content', 'about_page_content', 'online_page_content',
                  'created_on', 'updated_on']

        extra_kwargs = {
            "name": {
                "required": False
            }
        }

    def to_representation(self, instance):
        self.fields['specialities'] = SpecialitySerializer(many=True)
        self.fields['owner'] = PubUserSerializer(many=False)
        self.fields['county'] = CountySerializer(many=False)
        self.fields['constituency'] = ConstituencySerializer(many=False)
        return super(FacilitySerializer, self).to_representation(instance)


class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = ['id', 'doctor', 'course', 'institution', 'year', 'notes', 'file', 'created_on', 'updated_on']


class DoctorSerializer(WritableNestedModelSerializer):
    user = PubUserSerializer(required=True)
    # qualifications = QualificationSerializer(many=True)

    class Meta:
        model = Doctor
        fields = ['id', 'facilities', 'user', 'available', 'about',
                  'qualifications', 'license_number',
                  'regulatory_body', 'license_file', 'is_verified', 'created_on', 'updated_on']
        extra_kwargs = {
            'qualifications': {
                'required': False
            },
            # 'doctor_appointments': {
            #     'required': False
            # }
        }

    def to_representation(self, instance):
        self.fields['facilities'] = FacilitySerializer(many=True)
        self.fields['user'] = PubUserSerializer(many=False)
        # self.fields['specialities'] = SpecialitySerializer(many=True)
        # self.fields['doctor_appointments'] = AppointmentSerializer(many=True)
        self.fields['qualifications'] = QualificationSerializer(many=True)
        return super(DoctorSerializer, self).to_representation(instance)


class StaffSerializer(WritableNestedModelSerializer):
    user = PubUserSerializer(required=True)

    class Meta:
        model = Staff
        fields = ['id', 'facility', 'user', 'status', 'designation', 'education',
                  'created_on', 'updated_on']

    def to_representation(self, instance):
        self.fields['facility'] = FacilitySerializer(many=False)
        self.fields['user'] = PubUserSerializer(many=False)
        return super(StaffSerializer, self).to_representation(instance)


class DoctorNoteSerializerForPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorNote
        fields = ['id', 'facility', 'doctor', 'description', 'date', 'encounter_medical_files', 'created_on']

    def to_representation(self, instance):
        self.fields['doctor'] = DoctorSerializer(many=False)
        self.fields['facility'] = FacilitySerializer(many=False)
        self.fields['encounter_medical_files'] = MedicalFileSerializer(many=True)
        return super(DoctorNoteSerializerForPatientSerializer, self).to_representation(instance)


class PatientSerializer(WritableNestedModelSerializer):
    user = PubUserSerializer(required=True)

    class Meta:
        model = Patient
        fields = ['id', 'facility', 'facilities', 'user', 'blood_group', 'dob', 'account_sharable', 'reason_for_signup',
                  'created_on', 'updated_on']

    def to_representation(self, instance):
        self.fields['facilities'] = FacilitySerializer(many=True)
        # self.fields['patient_encounters'] = EncounterSerializerForPatientSerializer(many=True)
        # self.fields['patient_appointments'] = AppointmentSerializer(many=True)
        self.fields['user'] = PubUserSerializer(many=False)
        return super(PatientSerializer, self).to_representation(instance)


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'facility', 'doctor', 'name', 'description', 'long_description', 'category', 'charges',
                  'duration', 'status', 'image', 'created_on', 'updated_on']

    def to_representation(self, instance):
        self.fields['category'] = ServiceCategorySerializer(many=False)
        self.fields['doctor'] = DoctorSerializer(many=False)
        self.fields['facility'] = FacilitySerializer(many=False)
        return super(ServiceSerializer, self).to_representation(instance)


class MedicalFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalFile
        fields = ['id', 'file', 'created_on']


class AppointmentSerializer(serializers.ModelSerializer):
    # patient = serializers.SerializerMethodField()
    # doctor = serializers.SerializerMethodField()
    # facility = serializers.SerializerMethodField()
    # condition = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'patient', 'facility', 'note', 'status', 'date', 'start_time', 'end_time',
                  'condition', 'other_condition', 'consultation_type', 'video_link', 'appointment_medical_files',
                  'created_on', 'updated_on']

    def to_representation(self, instance):
        # self.fields['doctor'] = DoctorSerializer(many=False)
        # self.fields['patient'] = PatientSerializer(many=False)
        # self.fields['facility'] = FacilitySerializer(many=False)
        # self.fields['condition'] = ConditionSerializer(many=False)
        self.fields['appointment_medical_files'] = MedicalFileSerializer(many=True)
        return super(AppointmentSerializer, self).to_representation(instance)

    def get_doctor(self, obj):
        serializer = PubUserSerializer(obj.doctor.user, many=False)
        return {
            "user": {
                "first_name": serializer.data['first_name'],
                "last_name": serializer.data['first_name'],
                "email": serializer.data['email'],
                # "profile": {
                #     "profile_photo": serializer.data["profile"]["profile_photo"]
                # }
            }
        }

    def get_patient(self, obj):
        serializer = PubUserSerializer(obj.patient.user, many=False)
        return {
            "user": {
                "first_name": serializer.data['first_name'],
                "last_name": serializer.data['first_name'],
                "email": serializer.data['email'],
            }
        }

    def get_facility(self, obj):
        serializer = FacilitySerializer(obj.facility, many=False)
        return {
            "cover_image": serializer.data["cover_image"],
            "name": serializer.data["name"],
            "email": serializer.data["email"],
        }

    def get_condition(self, obj):
        serializer = ConditionSerializer(obj.condition, many=False)
        return serializer.data["name"]


class DoctorNoteSerializer(serializers.ModelSerializer):
    # patient = serializers.SerializerMethodField()
    # doctor = serializers.SerializerMethodField()
    # facility = serializers.SerializerMethodField()

    class Meta:
        model = DoctorNote
        fields = ['id', 'facility', 'patient', 'doctor', 'description', 'date', 'encounter_medical_files', 'created_on']

    def to_representation(self, instance):
        self.fields['doctor'] = DoctorSerializer(many=False)
        self.fields['patient'] = PatientSerializer(many=False)
        self.fields['facility'] = FacilitySerializer(many=False)
        self.fields['encounter_medical_files'] = MedicalFileSerializer(many=True)
        return super(DoctorNoteSerializer, self).to_representation(instance)

    def get_doctor(self, obj):
        serializer = PubUserSerializer(obj.doctor.user, many=False)
        return {
            "user": {
                "first_name": serializer.data['first_name'],
                "last_name": serializer.data['first_name'],
                "email": serializer.data['email'],
                "profile": {
                    "profile_photo": serializer.data["profile"]["profile_photo"]
                }
            }
        }

    def get_patient(self, obj):
        serializer = PubUserSerializer(obj.patient.user, many=False)
        return {
            "user": {
                "first_name": serializer.data['first_name'],
                "last_name": serializer.data['first_name'],
                "email": serializer.data['email'],
                "profile": {
                    "profile_photo": serializer.data["profile"]["profile_photo"]
                }
            }
        }

    def get_facility(self, obj):
        serializer = FacilitySerializer(obj.facility, many=False)
        return {
            "cover_image": serializer.data["cover_image"],
            "name": serializer.data["name"]
        }


class PrescriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prescription
        fields = ['facility', 'doctor', 'patient', 'prescription']


class SharedPrescriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = SharedPrescription
        fields = ['facility', 'prescription']


