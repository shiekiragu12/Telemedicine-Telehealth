from rest_framework.serializers import ModelSerializer
from .models import EmailConfiguration, Email


class EmailSerializer(ModelSerializer):
    class Meta:
        model = Email
        fields = '__all__'


class EmailConfigSerializer(ModelSerializer):
    class Meta:
        model = EmailConfiguration
        fields = '__all__'
