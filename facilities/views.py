from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse

from .decorators import authorized_user, check_facility_and_attach_it_to_request
from .forms import CreateFacility
from .models import *


# Create your views here.

@login_required(login_url='signin')
@authorized_user
@check_facility_and_attach_it_to_request
def dashboard(request, facility_id):
    context = {
        'patients_count': Patient.objects.filter(facility=request.facility).count(),
        'docs_count': Doctor.objects.filter(facility=request.facility).count(),
        'appointments': Appointment.objects.filter(facility=request.facility).count(),
        'doctors': Doctor.objects.filter(facility=request.facility).order_by('-id')[0:5],
        'patients': Patient.objects.filter(facility=request.facility).order_by('-id')[0:5],
    }

    return render(request, template_name='dashboard/pages/index.html', context=context)


def login(request, facility_id):
    return render(request, template_name='dashboard/pages/login.html', context={})


def register(request, facility_id):
    return render(request, template_name='dashboard/pages/register.html', context={})


def create_facility(request):
    if request.method == 'POST':
        request.POST._mutable = True
        request.POST.update({"owner": request.user.id})
        request.POST._mutable = False
        form = CreateFacility(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Facility added successfully')
            return redirect('account_profile')
        else:
            for error in form.errors:
                messages.error(request, f"\n{error} {form.errors[error]}\n")
            return redirect('account_profile')


@login_required(login_url='signin')
@check_facility_and_attach_it_to_request
def facility(request, facility_id, facility_slug):
    return render(request, template_name='facilities/facility_home.html', context={})


@login_required(login_url='signin')
@check_facility_and_attach_it_to_request
def edit_facility(request, facility_id):
    if request.method == "POST":
        if request.POST.get('home_page_content', None) is not None:
            request.facility.home_page_content = request.POST.get('home_page_content')
            request.facility.save()
            messages.success(request, "Home page content updated successfully")
        if request.POST.get('about_page_content', None) is not None:
            request.facility.about_page_content = request.POST.get('about_page_content')
            request.facility.save()
            messages.success(request, "About page content updated successfully")
        if request.POST.get('online_page_content', None) is not None:
            request.facility.online_page_content = request.POST.get('online_page_content')
            request.facility.save()
            messages.success(request, "Online services page content updated successfully")

        return redirect('edit_facility', facility_id)
    return render(request, template_name='dashboard/pages/editfacility.html', context={})


@login_required(login_url='signin')
@check_facility_and_attach_it_to_request
def facility_about(request, facility_id, facility_slug):
    return render(request, template_name='facilities/facility_about.html', context={})


@login_required(login_url='signin')
@check_facility_and_attach_it_to_request
def facility_online_services(request, facility_id, facility_slug):
    return render(request, template_name='facilities/facility_online_services.html', context={})


@login_required(login_url='signin')
@check_facility_and_attach_it_to_request
def facility_services_treatments(request, facility_id, facility_slug):
    return render(request, template_name='facilities/facility_services_treatments.html', context={})


@login_required(login_url='signin')
@authorized_user
@check_facility_and_attach_it_to_request
def patients(request, facility_id):
    # messages.success(request, "almost done")
    context = {
        "patients": Patient.objects.filter(facility=request.facility)
    }
    return render(request, template_name='dashboard/pages/patient-list.html', context=context)


@login_required(login_url='signin')
@authorized_user
@check_facility_and_attach_it_to_request
def patients_create(request, facility_id):
    if request.method == "POST":
        existing_user = User.objects.filter(Q(username=get_value(request, 'email')) |
                                            Q(email=get_value(request, 'email'))).first()
        if existing_user is None:
            user = User.objects.create(username=get_value(request, 'email'),
                                       first_name=get_value(request, 'first_name'),
                                       last_name=get_value(request, 'last_name'),
                                       email=get_value(request, 'email'))
            user.save()
            user.set_password(get_value(request, 'username'))
            user.refresh_from_db()
            user.profile.profile_photo = request.FILES.get('profile_photo')
            user.profile.phone_number = get_value(request, 'phone_number')
            user.profile.gender = get_value(request, 'gender')
            user.profile.address = get_value(request, 'address')
            user.profile.city = get_value(request, 'city')
            user.profile.postal_code = get_value(request, 'postal_code')
            user.profile.save()

            user.refresh_from_db()

            patient = Patient.objects.create(facility=request.facility, user=user,
                                             dob=get_value(request, 'dob'),
                                             blood_group=get_value(request, 'blood_group'))
            patient.save()
            messages.success(request, 'Patient created successfully')

        else:
            messages.error(request, "Cannot register patient as user with similar records already exists.")

    return redirect('patients', facility_id)


def get_value(request, key):
    return request.POST.get(key)


@login_required(login_url='signin')
@authorized_user
@check_facility_and_attach_it_to_request
def doctors(request, facility_id):
    context = {
        "specialities": FacilitySpeciality.objects.all(),
        "doctors": Doctor.objects.filter(facility=request.facility)
    }
    return render(request, template_name='dashboard/pages/doctor-list.html', context=context)


@login_required(login_url='signin')
@authorized_user
@check_facility_and_attach_it_to_request
def doctors_create(request, facility_id):
    if request.method == "POST":

        existing_user = User.objects.filter(Q(username=get_value(request, 'email')) |
                                            Q(email=get_value(request, 'email'))).first()
        if existing_user is None:
            user = User.objects.create(username=get_value(request, 'email'),
                                       first_name=get_value(request, 'first_name'),
                                       last_name=get_value(request, 'last_name'),
                                       email=get_value(request, 'email'))
            user.save()
            user.set_password(get_value(request, 'username'))
            user.refresh_from_db()
            user.profile.profile_photo = request.FILES.get('profile_photo')
            user.profile.phone_number = get_value(request, 'phone_number')
            user.profile.gender = get_value(request, 'gender')
            user.profile.address = get_value(request, 'address')
            user.profile.city = get_value(request, 'city')
            user.profile.postal_code = get_value(request, 'postal_code')
            user.profile.save()

            user.refresh_from_db()

            speciality = FacilitySpeciality.objects.filter(id=get_value(request, 'speciality')).first()
            doctor = Doctor.objects.create(facility=request.facility, user=user,
                                           speciality=speciality,
                                           description=get_value(request, 'description'))
            doctor.save()
            messages.success(request, 'Doctor created successfully')

        else:
            messages.error(request, "Cannot register doctor as user with similar records already exists.")

    return redirect('doctors', facility_id)


@login_required(login_url='signin')
@authorized_user
@check_facility_and_attach_it_to_request
def staff(request, facility_id):
    context = {
        "staffs": Staff.objects.filter(facility=request.facility)
    }
    return render(request, template_name='dashboard/pages/staff.html', context=context)


@login_required(login_url='signin')
@authorized_user
@check_facility_and_attach_it_to_request
def staff_create(request, facility_id):
    if request.method == "POST":

        existing_user = User.objects.filter(Q(username=get_value(request, 'username')) |
                                            Q(email=get_value(request, 'email'))).first()
        if existing_user is None:
            user = User.objects.create(username=get_value(request, 'email'),
                                       first_name=get_value(request, 'first_name'),
                                       last_name=get_value(request, 'last_name'),
                                       email=get_value(request, 'email'))
            user.save()
            user.set_password(get_value(request, 'username'))
            user.refresh_from_db()
            user.profile.profile_photo = request.FILES.get('profile_photo')
            user.profile.phone_number = get_value(request, 'phone_number')
            user.profile.gender = get_value(request, 'gender')
            user.profile.dob = get_value(request, 'dob')
            user.profile.address = get_value(request, 'address')
            user.profile.city = get_value(request, 'city')
            user.profile.postal_code = get_value(request, 'postal_code')
            user.profile.save()

            user.refresh_from_db()

            staffMember = Staff.objects.create(facility=request.facility, user=user,
                                               designation=get_value(request, 'designation'),
                                               education=get_value(request, 'education'))
            staffMember.save()
            messages.success(request, 'Staff created successfully')

        else:
            messages.error(request, "Cannot register staff as user with similar records already exists.")

    return redirect('staff', facility_id)


@login_required(login_url='signin')
@authorized_user
@check_facility_and_attach_it_to_request
def appointments(request, facility_id):
    context = {
        'doctors': Doctor.objects.filter(facility=request.facility),
        'patients': Patient.objects.filter(facility=request.facility),
        'conditions': Condition.objects.all(),
        'appointments': Appointment.objects.filter(facility=request.facility)
    }
    return render(request, template_name='dashboard/pages/appointment.html', context=context)


@login_required(login_url='signin')
@authorized_user
@check_facility_and_attach_it_to_request
def appointments_create(request, facility_id):
    if request.method == "POST":
        patient = Patient.objects.filter(id=get_value(request, 'patient')).first()
        doctor = Doctor.objects.filter(id=get_value(request, 'doctor')).first()
        condition_ = Condition.objects.filter(id=get_value(request, 'condition')).first()

        appointment = Appointment.objects.create(facility=request.facility, doctor=doctor,
                                                 patient=patient, note=get_value(request, 'note'),
                                                 start_time=get_value(request, 'start_time'),
                                                 end_time=get_value(request, 'end_time'),
                                                 condition=condition_, date=get_value(request, 'date'))
        appointment.save()
        messages.success(request, "Appointment created successfully")
    return redirect('appointments', facility_id)


@login_required(login_url='signin')
@authorized_user
@check_facility_and_attach_it_to_request
def services(request, facility_id):
    return render(request, template_name='dashboard/pages/services.html', context={})


@login_required(login_url='signin')
@authorized_user
@check_facility_and_attach_it_to_request
def encounters(request, facility_id):
    return render(request, template_name='dashboard/pages/encounters.html', context={})
