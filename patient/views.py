from django.shortcuts import render, get_object_or_404, redirect

from facilities.models import *
from shop.models import PrescriptionOrder
from .decorators import patient_only

from .utils import take_care_of_mental_form


@patient_only
def patient_dashboard(request):
    appointments_ = Appointment.objects.filter(patient=request.user.patient)
    prescriptions_ = Prescription.objects.filter(appointment__patient=request.user.patient)
    medical_reports_ = DoctorNote.objects.filter(patient=request.user.patient)
    context = {
        "appointments": appointments_[0:5],
        "total_appointments": appointments_.count(),
        "prescriptions": prescriptions_[0:5],
        "total_prescriptions": prescriptions_.count(),
        "total_medical_reports": medical_reports_.count(),
        "medical_reports": medical_reports_[0:5],
    }
    return render(request, template_name='patient-dashboard/pages/index.html', context=context)


@patient_only
def medical(request):
    medical_reports_ = DoctorNote.objects.filter(patient=request.user.patient)
    context = {
        "medical_reports": medical_reports_,
    }
    return render(request, template_name='patient-dashboard/pages/medical-reports.html', context=context)


@patient_only
def share_pdf(request):
    context = {'patients': Patient.objects.all()}
    pdf_url = request.GET.get('url')
    context = {'pdf_url': pdf_url}
    return render(request, template_name='patient-dashboard/pages/patient-list.html', context=context)


@patient_only
def prescriptions(request):
    prescriptions_ = Prescription.objects.filter(appointment__patient=request.user.patient)
    context = {
        "prescriptions": prescriptions_
    }
    return render(request, template_name='patient-dashboard/pages/prescriptions.html', context=context)


@patient_only
def prescription_orders(request):
    prescriptions_ = PrescriptionOrder.objects.filter(patient=request.user.patient)
    context = {
        "prescriptions": prescriptions_
    }
    return render(request, template_name='patient-dashboard/pages/prescription-orders.html', context=context)


@patient_only
def appointments(request):
    appointments_ = Appointment.objects.filter(patient=request.user.patient)
    context = {
        "appointments": appointments_
    }
    return render(request, template_name='patient-dashboard/pages/appointments.html', context=context)


@patient_only
def single_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    context = {
        "appointment": appointment
    }
    return render(request, template_name='patient-dashboard/pages/single-appointment.html', context=context)


@patient_only
def appointment_mental_form(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    context = {
        "appointment": appointment
    }
    return render(request, template_name='patient-dashboard/pages/mental-form/mental-health.html', context=context)


@patient_only
def fill_mental_form(request, appointment_id):
    existing_form = MentalForm.objects.filter(appointment=appointment_id).first()
    if request.method == 'POST':
        take_care_of_mental_form(request, appointment_id)
        return redirect(request.META['HTTP_REFERER'])
    context = {
        'form': existing_form,
        'appointment': Appointment.objects.filter(id=appointment_id).first()
    }
    return render(request, template_name='patient-dashboard/pages/mental-form/patient-mental-form.html', context=context)


@patient_only
def progress(request):
    return render(request, template_name='patient-dashboard/pages/patient-details.html', context={})
