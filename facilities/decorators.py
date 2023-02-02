from django.contrib import messages
from django.shortcuts import redirect
from .models import Facility, Doctor, Staff


def authorized_user(view_func):
    def wrapper_func(request, facility_id, *args, **kwargs):
        facility = Facility.objects.filter(id=facility_id).first()
        doctor = Doctor.objects.filter(user=request.user).first()
        receptionist = Staff.objects.filter(user=request.user).first()
        if facility.owner == request.user:
            return view_func(request, facility_id, *args, **kwargs)
        elif doctor and request.user.doctor.facility == facility:
            return view_func(request, facility_id, *args, **kwargs)
        elif receptionist and request.user.receptionist.facility == facility:
            return view_func(request, facility_id, *args, **kwargs)
        else:
            messages.error(request, "You are not authorized to view this facility's admin")
            return redirect('index')
    return wrapper_func


def check_facility_and_attach_it_to_request(view_func):
    def wrapper_func(request, facility_id, *args, **kwargs):
        facility = Facility.objects.filter(id=facility_id).first()
        if facility is None:
            messages.error(request, 'Facility does not exist')
            return redirect('index')
        else:
            request.facility = facility
            return view_func(request, facility_id, *args, **kwargs)
    return wrapper_func
