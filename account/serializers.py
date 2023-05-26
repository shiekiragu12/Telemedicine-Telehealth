from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from .models import *
from facilities.serializers import DoctorSerializer, PatientSerializer, StaffSerializer


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'


class UserSerializer(WritableNestedModelSerializer):
    profile = ProfileSerializer(required=False)
    doctor = DoctorSerializer(required=False)
    patient = PatientSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'profile', 'doctor', 'patient',
                  'staff', 'date_joined', 'last_login']

        extra_kwargs = {
            'password': {
                'required': False,
                'write_only': True
            }
        }

    def create(self, validated_data, *args, **kwargs):
        validated_data['password'] = make_password(validated_data.get('password', validated_data.get('username')))
        return super().create(validated_data, *args, **kwargs)

    def to_representation(self, instance):
        self.fields['doctor'] = DoctorSerializer(many=False)
        self.fields['patient'] = PatientSerializer(many=False)
        self.fields['profile'] = ProfileSerializer(many=False)
        self.fields['staff'] = StaffSerializer(many=False)
        return super(UserSerializer, self).to_representation(instance)
