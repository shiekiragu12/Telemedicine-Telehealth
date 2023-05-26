from django.shortcuts import render, get_object_or_404
from facilities.models import *
from shop.models import PrescriptionOrder


# Create your views here.


def patient_dashboard(request):
    appointments_ = Appointment.objects.filter(patient=request.user.patient)
    prescriptions_ = Prescription.objects.filter(patient=request.user.patient)
    medical_reports_ = Encounter.objects.filter(patient=request.user.patient)
    context = {
        "appointments": appointments_[0:5],
        "total_appointments": appointments_.count(),
        "prescriptions": prescriptions_[0:5],
        "total_prescriptions": prescriptions_.count(),
        "total_medical_reports": medical_reports_.count(),
        "medical_reports": medical_reports_[0:5],
    }
    return render(request, template_name='patient-dashboard/pages/index.html', context=context)


def medical(request):
    medical_reports_ = Encounter.objects.filter(patient=request.user.patient)
    context = {
        "medical_reports": medical_reports_,
    }
    return render(request, template_name='patient-dashboard/pages/medical-reports.html', context=context)


def share_pdf(request):
    context = {'patients': Patient.objects.all()}
    pdf_url = request.GET.get('url')
    context = {'pdf_url': pdf_url}
    return render(request, template_name='patient-dashboard/pages/patient-list.html', context=context)


def prescriptions(request):
    prescriptions_ = Prescription.objects.filter(patient=request.user.patient)
    context = {
        "prescriptions": prescriptions_
    }
    return render(request, template_name='patient-dashboard/pages/prescriptions.html', context=context)


def prescription_orders(request):
    prescriptions_ = PrescriptionOrder.objects.filter(patient=request.user.patient)
    context = {
        "prescriptions": prescriptions_
    }
    return render(request, template_name='patient-dashboard/pages/prescription-orders.html', context=context)


def appointments(request):
    appointments_ = Appointment.objects.filter(patient=request.user.patient)
    context = {
        "appointments": appointments_
    }
    return render(request, template_name='patient-dashboard/pages/appointments.html', context=context)


def single_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    context = {
        "appointment": appointment
    }
    return render(request, template_name='patient-dashboard/pages/single-appointment.html', context=context)


def progress(request):
    return render(request, template_name='patient-dashboard/pages/patient-details.html', context={})
