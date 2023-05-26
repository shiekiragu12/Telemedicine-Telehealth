from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework_bulk import BulkModelViewSet

from account.serializers import ProfileSerializer, UserSerializer
from account.models import Profile
from facilities.serializers import *
from facilities.models import *
from shop.serializers import *
from shop.models import *
from mainapp.models import Contact, AppConfig, Topic, Blog, Reply
from mainapp.serializers import ContactSerializer, AppConfigSerializer, TopicsSerializer, BlogSerializer, \
    ReplySerializer
from mailer.models import EmailConfiguration, Email
from mailer.serializers import EmailSerializer, EmailConfigSerializer
from website.models import Schedule, Analytic, Apply, Equip, Telehealth, DemoRequest, Book, Firstaid
from website.serializers import ScheduleSerializer, AnalyticSerializer, ApplySerializer, EquipSerializer, \
    TelehealthSerializer, DemoRequestSerializer, BookSerializer, FirstAidSerializer


# Account ViewSets
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Shop ViewSets

class ProductTypeViewSet(viewsets.ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


# Facilities ViewSets
class CountyViewSet(viewsets.ModelViewSet):
    queryset = County.objects.all()
    serializer_class = CountySerializer


class ConstituencyViewSet(viewsets.ModelViewSet):
    queryset = Constituency.objects.all()
    serializer_class = ConstituencySerializer


class ConditionViewSet(viewsets.ModelViewSet):
    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer


class IllnessViewSet(viewsets.ModelViewSet):
    queryset = Illness.objects.get_queryset()
    serializer_class = IllnessSerializer


class SpecialityViewSet(viewsets.ModelViewSet):
    queryset = FacilitySpeciality.objects.all()
    serializer_class = SpecialitySerializer


class FacilityTypeViewSet(viewsets.ModelViewSet):
    queryset = FacilityType.objects.get_queryset()
    serializer_class = FacilityTypeSerializer


class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['facility_code']


class QualificationViewSet(BulkModelViewSet):
    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializer


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class ServiceCategoryViewSet(viewsets.ModelViewSet):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class EncounterViewSet(viewsets.ModelViewSet):
    queryset = Encounter.objects.all()
    serializer_class = EncounterSerializer


# App settings
# Emails
class EmailConfigViewSet(viewsets.ModelViewSet):
    queryset = EmailConfiguration.objects.get_queryset()
    serializer_class = EmailConfigSerializer


class EmailViewSet(viewsets.ModelViewSet):
    queryset = Email.objects.get_queryset()
    serializer_class = EmailSerializer


class AppConfigViewSet(viewsets.ModelViewSet):
    queryset = AppConfig.objects.get_queryset()
    serializer_class = AppConfigSerializer


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.get_queryset()
    serializer_class = PrescriptionSerializer


class SharedPrescriptionViewSet(viewsets.ModelViewSet):
    queryset = SharedPrescription.objects.get_queryset()
    serializer_class = SharedPrescriptionSerializer


class PrescriptionOrderViewSet(viewsets.ModelViewSet):
    queryset = PrescriptionOrder.objects.get_queryset()
    serializer_class = PrescriptionOrderSerializer


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.get_queryset()
    serializer_class = TopicsSerializer


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.get_queryset()
    serializer_class = BlogSerializer


class ReplyViewSet(viewsets.ModelViewSet):
    queryset = Reply.objects.get_queryset()
    serializer_class = ReplySerializer


# Contact Forms
class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.get_queryset()
    serializer_class = ContactSerializer


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.get_queryset()
    serializer_class = ScheduleSerializer


class AnalyticViewSet(viewsets.ModelViewSet):
    queryset = Analytic.objects.get_queryset()
    serializer_class = AnalyticSerializer


class ApplyViewSet(viewsets.ModelViewSet):
    queryset = Apply.objects.get_queryset()
    serializer_class = ApplySerializer


class EquipViewSet(viewsets.ModelViewSet):
    queryset = Equip.objects.get_queryset()
    serializer_class = EquipSerializer


class TelehealthViewSet(viewsets.ModelViewSet):
    queryset = Telehealth.objects.get_queryset()
    serializer_class = TelehealthSerializer


class TopButtonViewSet(viewsets.ModelViewSet):
    queryset = DemoRequest.objects.get_queryset()
    serializer_class = DemoRequestSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.get_queryset()
    serializer_class = BookSerializer


class FirstAidViewSet(viewsets.ModelViewSet):
    queryset = Firstaid.objects.get_queryset()
    serializer_class = FirstAidSerializer
