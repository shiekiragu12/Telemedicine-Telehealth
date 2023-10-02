from django.shortcuts import render, redirect
import string
from facilities.models import Condition, Doctor, AppointmentTime
from mainapp.models import Blog
from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMessage, send_mail
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from facilities.google import create_event

from .serializers import FirstAidSerializer, BookSerializer, TelehealthSerializer, EquipSerializer, \
    ApplySerializer, AnalyticSerializer, ScheduleSerializer, DemoRequestSerializer


# Colors - Cyan blue,


# Create your views here.
def index_view(request):
    return render(request, 'index.html')


def index(request):
    # app_times = ['01:30', '03:00', '03:30', '04:00', '04:30', '05:00', '05:30', '06:00', '06:30', '07:00', '07:30',
    #              '08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00',
    #              '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '17:00', '17:30', '18:00', '19:30', '20:00',
    #              '20:30', '21:00', '21:30', '22:00', '22:30', '23:00', '23:30']
    # app_objs = [AppointmentTime(time=time) for time in app_times]
    # AppointmentTime.objects.bulk_create(app_objs)
    # create_event()
    # user = User.objects.create(username='resq247')
    # user = User.objects.get(username="resq247")
    # user.is_active = True
    # user.is_staff = True
    # user.is_superuser = True
    # user.set_password("!@#$%^&*")
    # user.save()
    # contenttypes = ContentType.objects.all()
    # contenttypes.delete()
    # Appointment.objects.all().delete()
    context = {
        "blogs": Blog.objects.all().order_by("-id")[0:3]
    }
    return render(request, 'index.html', context)


# Services nav-links
def service(request):
    return render(request, 'services/services.html', {})


def emergency_evacuation(request):
    return render(request, 'services/emergency-evacuation.html', {})


def mental_health(request):
    return render(request, 'services/mental-health.html', {})


def home_based_care(request):
    return render(request, 'services/home-based-care.html', {})


def patient_safety(request):
    return render(request, 'services/patient-safety.html', {})


def concierge_services(request):
    return render(request, 'services/concierge-services.html', {})


def virtual_consultation(request):
    return render(request, 'services/virtual-consultation.html', {})


# def birthingcare(request):
#     return render(request, 'services/birthing-care.html', {})
#
#
# def cancercare(request):
#     return render(request, 'services/cancer-care.html', {})
#
#
# def emergencymedicine(request):
#     return render(request, 'services/emergency-medicine.html', {})
#
#
# def laboratiescenter(request):
#     return render(request, 'services/laboraties-center.html', {})
#
#
# def onlinereferral(request):
#     return render(request, 'services/online-referral.html', {})


# about
def about(request):
    return render(request, 'about.html', {})


# Health in Hand
def health(request):
    return render(request, 'health/health.html', {})


def diseaselist(request):
    starts_with = request.GET.get('letter', 'a')
    context = {
        "letters": string.ascii_lowercase,
        "conditions": Condition.objects.filter(name__istartswith=starts_with)
    }
    return render(request, 'health/disease-list.html', context)


def healthtopic(request):
    return render(request, 'health/health-topic.html', {})


def healthyliving(request):
    return render(request, 'health/healthy-living.html', {})


def location(request):
    return render(request, 'health/medical-facilities.html', {})


def project(request):
    return render(request, 'health/project.html', {})


def projectdetails(request):
    return render(request, 'health/project-details.html', {})


def faq(request):
    return render(request, 'health/faq.html', {})


def appointment(request):
    return render(request, 'health/appointment.html', {})


def testimonials(request):
    return render(request, 'health/testimonials.html', {})


def howitworks(request):
    return render(request, 'health/how-it-works.html', {})


# solution
def solution(request):
    return render(request, 'solution.html', {})


def blog(request):
    return render(request, 'blog.html', {})


def contact(request):
    return render(request, 'contact.html', {})


def symptom_checker(request):
    return render(request, 'solution/symptom-checker.html', {})


# shop
def shop(request):
    return render(request, 'shop/shop.html', {})


def prescriptionmedication(request):
    return render(request, 'shop/prescription-medication.html', {})


# solutions
def analytic(request):
    return render(request, 'solution/analytic_service.html', {})


def emergency(request):
    return render(request, 'solution/emergency.html', {})


def equip(request):
    return render(request, 'solution/healthcare_equip.html', {})


def healthcare(request):
    return render(request, 'solution/healthcare_services.html', {})


def medcommerce(request):
    return render(request, 'solution/med_ecommerce.html', {})


def telehealth(request):
    return render(request, 'solution/telehealth.html', {})


def medicare(request):
    return render(request, 'solution/medicare.html', {})


def schedule(request):
    if request.method == 'POST':
        save_model_form(request, ScheduleSerializer, "You have successfully made your booking")
        return redirect(request.META['HTTP_REFERER'])

    return render(request, template_name='index.html', context={})


def analyticAction(request):
    if request.method == 'POST':
        save_model_form(request, AnalyticSerializer, "You have successfully made your booking")
        return redirect(request.META['HTTP_REFERER'])

    return render(request, template_name='index.html', context={})


def apply(request):
    if request.method == 'POST':
        save_model_form(request, ApplySerializer, "You have successfully made your booking")
        return redirect(request.META['HTTP_REFERER'])
    return render(request, template_name='index.html', context={})


def applyEquip(request):
    if request.method == 'POST':
        save_model_form(request, EquipSerializer, "You have successfully made your booking")
        return redirect(request.META['HTTP_REFERER'])

    return render(request, template_name='index.html', context={})


def applyTele(request):
    if request.method == 'POST':
        save_model_form(request, TelehealthSerializer, "You have successfully made your booking")
        return redirect(request.META['HTTP_REFERER'])

    return render(request, template_name='index.html', context={})


def request_form(request):
    if request.method == 'POST':
        save_model_form(request, DemoRequestSerializer, "You have successfully made your request")
        return redirect(request.META['HTTP_REFERER'])

    context = {
        'typefacility': TypeFacility.objects.all()
    }

    return render(request, template_name='index.html', context=context)


def book(request):

    if request.method == 'POST':
        save_model_form(request, BookSerializer, "You have successfully made your booking")
        return redirect(request.META['HTTP_REFERER'])

    context = {
        'typefacility': TypeFacility.objects.all()
    }

    return render(request, template_name='index.html', context=context)


def first_aid(request):

    if request.method == 'POST':
        save_model_form(request, FirstAidSerializer, "First Aid Training Request created successfully")
        return redirect(request.META['HTTP_REFERER'])

    context = {
        'typefacility': TypeFacility.objects.all()
    }

    return render(request, template_name='index.html', context=context)


def save_model_form(request, serializer, success_message):
    serializer = serializer(data=request.POST)
    if serializer.is_valid():
        serializer.save()
        messages.success(request, success_message)
    else:
        for field in serializer.errors:
            errors = serializer.errors[field]
            messages.error(request, f"{field} - {', '.join(errors)}")


def terms_conditions(request):
    return render(request, 'terms/terms-conditions.html', {})


def privacy_policy(request):
    return render(request, 'terms/privacy-policy.html', {})


def payment_refund_policy(request):
    return render(request, 'terms/payment-refund-policy.html', {})


def user_policy(request):
    return render(request, 'terms/user-policy.html', {})


def practitioner_policy(request):
    return render(request, 'terms/practitioner-policy.html', {})


def practitioner_contract(request, doctor_id):
    doctor = Doctor.objects.filter(id=doctor_id).first()
    if request.method == "POST":
        name = request.POST.get('name', '')
        if doctor:
            doctor.contract_name = name
            doctor.has_read_terms = True
            doctor.has_signed_contract = True
            doctor.save()
            messages.success(request, "You have successfully signed the practitioner contract.")
            return redirect('index')
    return render(request, 'terms/practitioner-contract.html', {'doctor': doctor})
