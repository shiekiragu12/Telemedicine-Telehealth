from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['phone_number', 'gender', 'address', 'country', 'city', 'profile_photo', 'dob']


class PubUserSerializer(WritableNestedModelSerializer):
    profile = ProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'profile', 'date_joined',
                  'last_login']
        read_only_fields = ['date_joined', 'last_login']
        write_only_fields = ['password']

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
        self.fields['profile'] = ProfileSerializer(many=False)
        return super(PubUserSerializer, self).to_representation(instance)
