from rest_framework.serializers import ModelSerializer

from .models import AppConfig


class AppConfigSerializer(ModelSerializer):
    class Meta:
        model = AppConfig
        fields = '__all__'
