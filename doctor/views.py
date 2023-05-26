from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404

from pharmacetical.models import Pharmacy
from facilities.models import *
from .decorators import authorization_required

# Create your views here.


@authorization_required
def doctor_dashboard(request):
    appointments_ = Appointment.objects.filter(doctor=request.user.doctor)
    prescriptions_ = Prescription.objects.filter(doctor=request.user.doctor)
    medical_reports_ = Encounter.objects.filter(doctor=request.user.doctor)
    context = {
        "appointments": appointments_[0:5],
        "total_appointments": appointments_.count(),
        "prescriptions": prescriptions_[0:5],
        "total_prescriptions": prescriptions_.count(),
        "total_medical_reports": medical_reports_.count(),
        "medical_reports": medical_reports_[0:5],
    }
    return render(request, template_name='doctor-dashboard/pages/index.html', context=context)


@authorization_required
def medical_reports(request):
    medical_reports_ = Encounter.objects.filter(doctor=request.user.doctor)
    context = {
        "medical_reports": medical_reports_,
    }
    return render(request, template_name='doctor-dashboard/pages/medical-reports.html', context=context)


@authorization_required
def prescriptions(request):
    prescriptions_ = Prescription.objects.filter(doctor=request.user.doctor)
    context = {
        "prescriptions": prescriptions_
    }
    return render(request, template_name='doctor-dashboard/pages/prescriptions.html', context=context)


@authorization_required
def appointments(request):
    appointments_ = Appointment.objects.filter(doctor=request.user.doctor)
    context = {
        "appointments": appointments_
    }
    return render(request, template_name='doctor-dashboard/pages/appointments.html', context=context)


@authorization_required
def single_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        link = request.POST.get('video_link', None)
        if link:
            appointment.video_link = link
            appointment.save()
            messages.success(request, 'Link successfully updated')
        else:
            messages.error(request, "You have not provided any link.")

        return redirect(request.META.get("HTTP_REFERER"))
    context = {
        "appointment": appointment
    }
    return render(request, template_name='doctor-dashboard/pages/single-appointment.html', context=context)


@authorization_required
def consultation_notes(request):
    consultations_ = []
    context = {
        "consultations": consultations_
    }
    return render(request, template_name='doctor-dashboard/pages/consultation-notes.html', context=context)


@authorization_required
def lab_orders(request):
    lab_orders_ = []
    context = {
        "lab_orders": lab_orders_
    }
    return render(request, template_name='doctor-dashboard/pages/lab-orders.html', context=context)


@authorization_required
def text_consultations(request):
    consultations_ = []
    context = {
        "consultations": consultations_
    }
    return render(request, template_name='doctor-dashboard/pages/text-consultation.html', context=context)


@authorization_required
def video_consultations(request):
    consultations_ = []
    context = {
        "consultations": consultations_
    }
    return render(request, template_name='doctor-dashboard/pages/video-consultation.html', context=context)


@authorization_required
def create_prescription(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        pharma_name = request.POST.get('pharma_name')
        location = request.POST.get('location')
        licence = request.POST.get('licence')
        email = request.POST.get('email')
        alternative_email = request.POST.get('alternative_email')
        number = request.POST.get('number')
        alternative_number = request.POST.get('alternative_number')
        created_on = request.POST.get('created_on')
        attach = request.FILES.get('image')
        subject = 'Form submission received'
        body = 'Thank you for submitting the form your form is currently under review'
        email = EmailMessage(subject, body, to=[request.POST['email']])
        email.send()

        existingpharmacy = Pharmacy.objects.filter(
            pharma_name=pharma_name).exists()

        # user = User.objects.order_by('-pk')[0]

        pharmacy = Pharmacy(first_name=first_name, last_name=last_name, pharma_name=pharma_name,
                            location=location, licence=licence, email=email, alternative_email=alternative_email, number=number, alternative_number=alternative_number, date_created=created_on, attach=attach)

        pharmacy.save()
        messages.success(
            request, 'Pharmacy created successfully wait for approval')
        return redirect('index')

    return render(request, template_name='pharmacy/verification-form.html', context={})
