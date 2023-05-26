from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from mainapp.models import Tag
from .decorators import authorized_user, check_facility_and_attach_it_to_request, \
    check_facility_and_attach_it_to_request_2
from .forms import CreateFacility, ServiceForm
import openpyxl
from .models import *


# Create your views here.

@login_required(login_url='signin')
@authorized_user
@check_facility_and_attach_it_to_request
def dashboard(request, facility_id):
    context = {
        'patients_count': Patient.objects.filter(facility=request.facility).count(),
        'docs_count': Doctor.objects.filter(facilities__in=[request.facility]).count(),
        'appointments': Appointment.objects.filter(facility=request.facility).count(),
        'doctors': Doctor.objects.filter(facilities__id=request.facility.id).order_by('-id')[0:5],
        'patients': Patient.objects.filter(Q(facility=request.facility) | Q(facilities__id=request.facility.id))[0:5],
    }

    return render(request, template_name='dashboard/pages/index.html', context=context)


def login(request, facility_id):
    return render(request, template_name='dashboard/pages/login.html', context={})


def register(request, facility_id):
    return render(request, template_name='dashboard/pages/register.html', context={})


def facilities(request):
    facilities_ = Facility.objects.all()
    paginator = Paginator(facilities_, 25)  # Show 25 contacts per page.

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "pages": paginator.page_range,
        "page_count": paginator.num_pages,
        "counties": County.objects.all()
    }
    return render(request, template_name="facilities/facilities.html", context=context)


def facilities_per_location(request, location_type, location_id, location_slug):
    if location_type == "county":
        county = get_object_or_404(County, id=location_id)
        facilities_ = Facility.objects.filter(county=county)
        paginator = Paginator(facilities_, 25)  # Show 25 contacts per page.

        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        context = {
            "page_obj": page_obj,
            "pages": paginator.page_range,
            "page_count": paginator.num_pages,
            "counties": County.objects.all(),
            "location_type": location_type,
            "county": county,
        }
        return render(request, template_name="facilities/facilities_county.html", context=context)
    else:
        constituency = get_object_or_404(Constituency, id=location_id)
        facilities_ = Facility.objects.filter(constituency=constituency)
        paginator = Paginator(facilities_, 25)  # Show 25 contacts per page.

        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        context = {
            "page_obj": page_obj,
            "pages": paginator.page_range,
            "page_count": paginator.num_pages,
            "counties": County.objects.all(),
            "location_type": location_type,
            "constituency": constituency,
        }
        return render(request, template_name="facilities/facilities_constituency.html", context=context)


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
@check_facility_and_attach_it_to_request_2
def facility(request, facility_id, facility_slug):
    return render(request, template_name='facilities/facility_home.html', context={})


@login_required(login_url='signin')
@check_facility_and_attach_it_to_request
def edit_facility(request, facility_id):
    context = {
        'facility_types': FacilityType.objects.all(),
        'counties': County.objects.all(),
        'specialities': FacilitySpeciality.objects.all(),
        'options': [
            {"label": "Pharmacy", "value": 'pharmacy'},
            {"label": "Clinic", "value": 'clinic'},
            {"label": "Nutraceutical", "value": 'nutraceutical'},
        ]
    }
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
    return render(request, template_name='dashboard/pages/editfacility.html', context=context)


@login_required(login_url='signin')
@check_facility_and_attach_it_to_request_2
def facility_about(request, facility_id, facility_slug):
    return render(request, template_name='facilities/facility_about.html', context={})


@login_required(login_url='signin')
@check_facility_and_attach_it_to_request_2
def facility_online_services(request, facility_id, facility_slug):
    return render(request, template_name='facilities/facility_online_services.html', context={})


@login_required(login_url='signin')
@check_facility_and_attach_it_to_request_2
def facility_services_treatments(request, facility_id, facility_slug):
    return render(request, template_name='facilities/facility_services_treatments.html', context={})


@login_required(login_url='signin')
@authorized_user
@check_facility_and_attach_it_to_request
def patients(request, facility_id):
    # messages.success(request, "almost done")
    context = {
        "patients": Patient.objects.filter(Q(facility=request.facility) | Q(facilities__id=request.facility.id))
    }
    return render(request, template_name='dashboard/pages/patient-list.html', context=context)


@login_required(login_url='signin')
@authorized_user
@check_facility_and_attach_it_to_request
def patient_details(request, facility_id, patient_id):
    # messages.success(request, "almost done")
    patient_ = Patient.objects.filter(id=patient_id).first()
    print(patient_.patient_prescriptions.all())
    context = {
        "patient": patient_
    }
    return render(request, template_name='dashboard/pages/patient-details.html', context=context)


@login_required(login_url='signin')
@authorized_user
@check_facility_and_attach_it_to_request
def staff_details(request, facility_id, staff_id):
    # messages.success(request, "almost done")
    context = {
        "staff": Staff.objects.filter(id=staff_id).first()
    }
    return render(request, template_name='dashboard/pages/staff-profile.html', context=context)


@login_required(login_url='signin')
@authorized_user
@check_facility_and_attach_it_to_request
def patients_create(request, facility_id):
    return redirect('patients', facility_id)


def get_value(request, key):
    return request.POST.get(key)


@login_required(login_url='signin')
@authorized_user
@check_facility_and_attach_it_to_request
def doctors(request, facility_id):
    context = {
        "specialities": FacilitySpeciality.objects.all(),
        "doctors": Doctor.objects.filter(facilities__id=request.facility.id)
    }
    return render(request, template_name='dashboard/pages/doctor-list.html', context=context)


@login_required(login_url='signin')
@authorized_user
@check_facility_and_attach_it_to_request
def doctors_create(request, facility_id):
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

    return redirect('staff', facility_id)


@login_required(login_url='signin')
@authorized_user
@check_facility_and_attach_it_to_request
def appointments(request, facility_id):
    context = {
        'doctors': Doctor.objects.filter(facilities__id=request.facility.id),
        'patients': Patient.objects.filter(Q(facility=request.facility) | Q(facilities__id=request.facility.id)),
        'conditions': Condition.objects.all(),
        'appointments': Appointment.objects.filter(facility=request.facility)
    }
    return render(request, template_name='dashboard/pages/appointment.html', context=context)


@login_required(login_url='signin')
@authorized_user
@check_facility_and_attach_it_to_request
def create_prescription(request, facility_id):
    context = {
        'patients': Patient.objects.filter(Q(facility=request.facility) | Q(facilities__id=request.facility.id)),
    }
    return render(request, template_name='dashboard/pages/create-prescription.html', context=context)


@login_required(login_url='signin')
@authorized_user
@check_facility_and_attach_it_to_request
def create_medical_report(request, facility_id):
    context = {
        'patients': Patient.objects.filter(Q(facility=request.facility) | Q(facilities__id=request.facility.id)),
    }
    return render(request, template_name='dashboard/pages/create-medical-report.html', context=context)


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
    if request.method == "POST":
        service_form = ServiceForm(request.POST, request.FILES)
        if service_form.is_valid():
            service_form.save()
            messages.success(request, "Service successfully created.")
        else:
            messages.error(request, "Error creating the service")
    context = {
        "services": Service.objects.filter(facility=request.facility),
        "doctors": Doctor.objects.filter(facilities__id=request.facility.id),
        "categories": ServiceCategory.objects.all(),
        "tags": Tag.objects.all(),
    }
    return render(request, template_name='dashboard/pages/services/services.html', context=context)


@login_required(login_url='signin')
@authorized_user
@check_facility_and_attach_it_to_request
def create_services(request, facility_id):
    context = {
        "services": Service.objects.filter(facility=request.facility),
        "doctors": Doctor.objects.filter(facilities__id=request.facility.id),
        "categories": ServiceCategory.objects.all(),
        "tags": Tag.objects.all(),
    }
    return render(request, template_name='dashboard/pages/services/create-service.html', context=context)


@login_required(login_url='signin')
@authorized_user
@check_facility_and_attach_it_to_request
def encounters(request, facility_id):
    return render(request, template_name='dashboard/pages/encounters.html', context={})
