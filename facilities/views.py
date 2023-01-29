from django.shortcuts import render

# Create your views here.


def dashboard(request, facility_id):
    return render(request, template_name='dashboard/pages/index.html', context={})


def login(request, facility_id):
    return render(request, template_name='dashboard/pages/login.html', context={})


def register(request, facility_id):
    return render(request, template_name='dashboard/pages/register.html', context={})


def patients(request, facility_id):
    return render(request, template_name='dashboard/pages/patient-list.html', context={})


def doctors(request, facility_id):
    return render(request, template_name='dashboard/pages/doctor-list.html', context={})


def staff(request, facility_id):
    return render(request, template_name='dashboard/pages/staff.html', context={})


def appointments(request, facility_id):
    return render(request, template_name='dashboard/pages/appointment.html', context={})


def services(request, facility_id):
    return render(request, template_name='dashboard/pages/services.html', context={})


def encounters(request, facility_id):
    return render(request, template_name='dashboard/pages/encounters.html', context={})
