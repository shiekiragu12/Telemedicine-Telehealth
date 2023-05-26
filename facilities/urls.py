from django.urls import path
from .views import *

urlpatterns = [
    path('', facilities, name="facilities"),
    path('locations/<str:location_type>/<str:location_id>/<str:location_slug>/', facilities_per_location,
         name="facilities_per_location"),
    path('create-facility/', create_facility, name="create_facility"),

    # Public facility information
    path('information/<str:facility_id>/<str:facility_slug>/', facility, name="facility"),
    path('information/<str:facility_id>/<str:facility_slug>/about-us/', facility_about, name="facility_about"),
    path('information/<str:facility_id>/<str:facility_slug>/online-services/', facility_online_services,
         name="facility_online_services"),
    path('information/<str:facility_id>/<str:facility_slug>/services-and-treatments/', facility_services_treatments,
         name="facility_services_treatments"),

    # Facility dashboard
    path('dashboard/admin/<str:facility_id>/', dashboard, name='dashboard'),
    path('dashboard/admin/<str:facility_id>/edit/', edit_facility, name='edit_facility'),
    # path('login/', dashboard, name='login'),
    # path('register/', dashboard, name='register'),

    path('dashboard/admin/<str:facility_id>/patients/', patients, name='patients'),
    path('dashboard/admin/<str:facility_id>/patients/create/', patients_create, name='patients_create'),
    path('dashboard/admin/<str:facility_id>/patients/view/<str:patient_id>/', patient_details, name='patient_details'),

    path('dashboard/admin/<str:facility_id>/patients/prescriptions/create/', create_prescription,
         name='create_prescription'),

    path('dashboard/admin/<str:facility_id>/patients/medical-reports/create/', create_medical_report,
         name='create_medical_report'),

    path('dashboard/admin/<str:facility_id>/doctors/', doctors, name='doctors'),
    path('dashboard/admin/<str:facility_id>/doctors/create/', doctors_create, name='doctors_create'),

    path('dashboard/admin/<str:facility_id>/staff/', staff, name='staff'),
    path('dashboard/admin/<str:facility_id>/staff/create/', staff_create, name='staff_create'),
    path('dashboard/admin/<str:facility_id>/staff/view/<str:staff_id>/', staff_details, name='staff_details'),

    path('dashboard/admin/<str:facility_id>/appointments/', appointments, name='appointments'),
    path('dashboard/admin/<str:facility_id>/appointments/create/', appointments_create, name='appointments_create'),

    path('dashboard/admin/<str:facility_id>/services/', services, name='services'),
    path('dashboard/admin/<str:facility_id>/services/create/', create_services, name='create_services'),

    path('dashboard/admin/<str:facility_id>/encounters/', encounters, name='encounters'),
]
