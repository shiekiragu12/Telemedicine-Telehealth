import datetime

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from facilities.forms import AppointmentForm
from facilities.models import *
from facilities.utils import is_not_blank_or_empty
from patient.utils import take_care_of_mental_form
from .decorators import doctor_and_authorization_required
from .forms import QualificationForm, DoctorNotesForm, LabTestRequestForm, PrescriptionForm
from .utils import create_meeting
from website.models import Notification


def add_qualification(request):
    if request.method == 'POST':
        form = QualificationForm(request.POST, request.FILES)
        if form.is_valid():
            qualification = form.save()
            Notification.objects.create(to_admin=True, title="Doctor has updated there qualification",
                                        message=f"{form.doctor.user.profile.salutation.title} "
                                                f"{form.doctor.user.get_full_name()}"
                                                f"has added a new qualification. "
                                                f"<a href='{reverse('super-admin-doctors-single', form.doctor.id)}'>View profile</a>")
            context = {"qualification": qualification}
            return render(request, template_name="doctors/qualification-card.html", context=context)
    return render(request, template_name="account/forms/add-doctor-academic-qualification.html", context={})


@doctor_and_authorization_required
def doctor_dashboard(request):
    appointments_ = Appointment.objects.filter(doctor=request.user.doctor)
    prescriptions_ = Prescription.objects.filter(appointment__doctor=request.user.doctor)
    medical_reports_ = DoctorNote.objects.filter(doctor=request.user.doctor)
    context = {
        "appointments": appointments_[0:5],
        "total_appointments": appointments_.count(),
        "prescriptions": prescriptions_[0:5],
        "total_prescriptions": prescriptions_.count(),
        "total_medical_reports": medical_reports_.count(),
        "medical_reports": medical_reports_[0:5],
    }
    return render(request, template_name='doctor-dashboard/pages/index.html', context=context)


@doctor_and_authorization_required
def medical_reports(request):
    medical_reports_ = DoctorNote.objects.filter(doctor=request.user.doctor)
    context = {
        "medical_reports": medical_reports_,
    }
    return render(request, template_name='doctor-dashboard/pages/medical-reports.html', context=context)


@doctor_and_authorization_required
def prescriptions(request):
    prescriptions_ = Prescription.objects.filter(appointment__doctor=request.user.doctor)
    context = {
        "prescriptions": prescriptions_
    }
    return render(request, template_name='doctor-dashboard/pages/prescriptions.html', context=context)


@doctor_and_authorization_required
def appointments(request):
    appointments_ = Appointment.objects.filter(doctor=request.user.doctor)

    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    type_ = request.GET.get('type')
    category = request.GET.get('category')

    if is_not_blank_or_empty(from_date) and is_not_blank_or_empty(to_date):
        appointments_ = appointments_.filter(
            Q(created_on__gte=from_date) &
            Q(created_on__lte=to_date))

    if is_not_blank_or_empty(type_):
        appointments_ = appointments_.filter(
            Q(consultation_type=type_))

    if is_not_blank_or_empty(category):
        appointments_ = appointments_.filter(
            Q(consultation_category=category))

    context = {
        "appointments": appointments_
    }
    return render(request, template_name='doctor-dashboard/pages/appointments.html', context=context)


@doctor_and_authorization_required
def single_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        link = request.POST.get('video_link', None)
        if link:
            appointment.video_link = link
            appointment.save()
            messages.success(request, 'Link successfully updated')
            send_custom_email('appointment_video_link_update', appointment, [appointment.patient.user.email])
        else:
            messages.error(request, "You have not provided any link.")

        return redirect(request.META.get("HTTP_REFERER"))
    context = {
        "appointment": appointment
    }
    return render(request, template_name='doctor-dashboard/pages/single-appointment.html', context=context)


@doctor_and_authorization_required
def consultation_notes(request):
    consultations_ = []
    context = {
        "consultations": consultations_
    }
    return render(request, template_name='doctor-dashboard/pages/consultation-notes.html', context=context)


@doctor_and_authorization_required
def lab_orders(request):
    lab_orders_ = LabTestRequest.objects.filter(appointment__doctor=request.user.doctor)
    context = {
        "lab_orders": lab_orders_
    }
    return render(request, template_name='doctor-dashboard/pages/lab-orders.html', context=context)


@doctor_and_authorization_required
def text_consultations(request):
    appointments_ = Appointment.objects.filter(Q(doctor=request.user.doctor) & Q(consultation_type='text'))
    context = {
        "appointments": appointments_
    }
    return render(request, template_name='doctor-dashboard/pages/text-consultation.html', context=context)


@doctor_and_authorization_required
def video_consultations(request):
    appointments_ = Appointment.objects.filter(Q(doctor=request.user.doctor) & Q(consultation_type='video'))
    context = {
        "appointments": appointments_
    }
    return render(request, template_name='doctor-dashboard/pages/video-consultation.html', context=context)


def create_appointment(request):
    if request.method == "POST":

        doctor = request.POST.get('doctor')
        date = request.POST.get('date')
        start_time = AppointmentTime.objects.get(id=request.POST.get('start_time')).time
        duration = AppointmentDuration.objects.get(id=request.POST.get('duration')).minutes
        date_to_watch = datetime.datetime.strptime(date, '%Y-%m-%d').date()

        start_datetime = datetime.datetime.combine(date_to_watch, start_time)
        zoom_start_time = start_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")

        # Calculate the end time based on start time and duration
        end_datetime = start_datetime + datetime.timedelta(minutes=duration)

        appointments_for_date = Appointment.objects.filter(doctor_id=doctor, date=date_to_watch)

        for appointment in appointments_for_date:
            if appointment.start_time.time <= start_datetime.time() < appointment.end_time or \
                    appointment.start_time.time < end_datetime.time() <= appointment.end_time or \
                    start_datetime.time() <= appointment.start_time.time < end_datetime.time():
                # Overlap found, handle the error
                error_message = "The selected appointment time overlaps with an existing appointment."
                messages.error(request, error_message, "error")
                return redirect(request.META.get('HTTP_REFERER'))

        request.POST._mutable = True
        request.POST.update({'end_time': end_datetime.time()})
        request.POST._mutable = False
        appointment_form = AppointmentForm(request.POST)

        if appointment_form.is_valid():
            new_appointment = appointment_form.save()
            if new_appointment.consultation_type == 'video':
                meeting_info = create_meeting('Medical health appointment',
                                              zoom_start_time, new_appointment.duration.minutes, new_appointment.note)
                if meeting_info.get('status') == 'success':
                    new_appointment.video_link = meeting_info.get('start_url')
                new_appointment.zoom_meeting_creation_response = meeting_info.get('response')
                new_appointment.save()
            messages.success(request, "Appointment created successfully")
        else:
            print(appointment_form.errors)
            messages.error(request, 'Something went wrong. Check the time you selected whether it goes beyond the next '
                                    'appointment', extra_tags='error')
    return redirect(request.META.get('HTTP_REFERER'))


@doctor_and_authorization_required
def fill_lab_test_form(request, appointment_id):
    existing_form = LabTestRequest.objects.filter(appointment__id=appointment_id).first()

    if request.method == 'POST':

        fasting = request.POST.get('fasting', 'false')

        request.POST._mutable = True
        request.POST.update({'appointment': appointment_id})
        request.POST.update({'fasting': True if fasting == 'yes' else False})
        request.POST._mutable = False

        form = LabTestRequestForm(request.POST)

        if existing_form:
            form = LabTestRequestForm(request.POST, instance=existing_form)
        if form.is_valid():
            form.save()
            messages.success(request, "Laboratory Form saved successfully")
        else:
            messages.error(request, "Something went wrong")

        return redirect(request.META['HTTP_REFERER'])
    context = {
        'form': existing_form
    }
    return render(request, template_name='doctor-dashboard/pages/lab-form.html', context=context)


@doctor_and_authorization_required
def fill_mental_form(request, appointment_id):
    existing_form = MentalForm.objects.filter(appointment=appointment_id).first()
    if request.method == 'POST':
        take_care_of_mental_form(request, appointment_id)
        return redirect(request.META['HTTP_REFERER'])
    context = {
        'form': existing_form,
        'appointment': Appointment.objects.filter(id=appointment_id).first()
    }
    return render(request, template_name='doctor-dashboard/pages/mental-form.html', context=context)


@doctor_and_authorization_required
def fill_doctor_notes_form(request, appointment_id):
    existing_form = DoctorNote.objects.filter(appointment__id=appointment_id).first()
    existing_prescription = Prescription.objects.filter(appointment__id=appointment_id).first()

    if request.method == 'POST':

        appointment = Appointment.objects.get(id=appointment_id)
        attended_treatment = request.POST.get('attended_treatment', 'false')

        request.POST._mutable = True
        request.POST.update({'appointment': appointment_id})
        request.POST.update({'patient': appointment.patient.id})
        request.POST.update({'doctor': appointment.doctor.id})
        request.POST.update({'attended_treatment': True if attended_treatment == 'yes' else False})
        request.POST._mutable = False

        doctor_notes_fields = {
            key: request.POST.get(key) for key in DoctorNotesForm.Meta.fields
        }
        prescription_fields = {
            key: request.POST.get(key) for key in PrescriptionForm.Meta.fields
        }

        form = DoctorNotesForm(doctor_notes_fields)
        prescription_form = PrescriptionForm(prescription_fields)
        if existing_prescription:
            prescription_form = PrescriptionForm(prescription_fields, instance=existing_prescription)

        if existing_form:
            form = DoctorNotesForm(doctor_notes_fields, instance=existing_form)
        if form.is_valid():
            form.save()
            messages.success(request, "Doctor Notes saved successfully")
        else:
            messages.error(request, "Something went wrong")

        if prescription_form.is_valid():
            prescription_form.save()

        return redirect(request.META['HTTP_REFERER'])
    context = {
        'form': existing_form,
        'prescription': existing_prescription
    }
    return render(request, template_name='doctor-dashboard/pages/doctor-notes.html', context=context)


