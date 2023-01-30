from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
        'patients': Patient.objects.filter(facility=request.facility).count(),
        'doctors': Doctor.objects.filter(facility=request.facility).count(),
        'appointments': Appointment.objects.filter(facility=request.facility).count(),
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
@authorized_user
@check_facility_and_attach_it_to_request
def patients(request, facility_id):
    return render(request, template_name='dashboard/pages/patient-list.html', context={})


@login_required(login_url='signin')
@authorized_user
@check_facility_and_attach_it_to_request
def doctors(request, facility_id):
    return render(request, template_name='dashboard/pages/doctor-list.html', context={})


@login_required(login_url='signin')
@authorized_user
@check_facility_and_attach_it_to_request
def staff(request, facility_id):
    return render(request, template_name='dashboard/pages/staff.html', context={})


@login_required(login_url='signin')
@authorized_user
@check_facility_and_attach_it_to_request
def appointments(request, facility_id):
    return render(request, template_name='dashboard/pages/appointment.html', context={})


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
