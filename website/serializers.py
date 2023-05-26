from rest_framework.serializers import ModelSerializer

from .models import *


class ScheduleSerializer(ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'


class AnalyticSerializer(ModelSerializer):
    class Meta:
        model = Analytic
        fields = '__all__'


class ApplySerializer(ModelSerializer):
    class Meta:
        model = Apply
        fields = '__all__'


class EquipSerializer(ModelSerializer):
    class Meta:
        model = Equip
        fields = '__all__'


class TelehealthSerializer(ModelSerializer):
    class Meta:
        model = Telehealth
        fields = '__all__'


class DemoRequestSerializer(ModelSerializer):
    class Meta:
        model = DemoRequest
        fields = '__all__'


class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class FirstAidSerializer(ModelSerializer):
    class Meta:
        model = Firstaid
        fields = '__all__'
