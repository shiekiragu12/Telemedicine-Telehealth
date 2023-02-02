from django.urls import path
from .views import *

urlpatterns = [
    path('', create_facility, name="create_facility"),

    path('information/<str:facility_id>/<str:facility_slug>/', facility, name="facility"),
    path('information/<str:facility_id>/<str:facility_slug>/about-us/', facility_about, name="facility_about"),
    path('information/<str:facility_id>/<str:facility_slug>/online-services/', facility_online_services,
         name="facility_online_services"),
    path('information/<str:facility_id>/<str:facility_slug>/services-and-treatments/', facility_services_treatments,
         name="facility_services_treatments"),

    path('dashboard/admin/<str:facility_id>/', dashboard, name='dashboard'),
    path('dashboard/admin/<str:facility_id>/edit/', edit_facility, name='edit_facility'),
    # path('login/', dashboard, name='login'),
    # path('register/', dashboard, name='register'),

    path('dashboard/admin/<str:facility_id>/patients/', patients, name='patients'),
    path('dashboard/admin/<str:facility_id>/patients/create/', patients_create, name='patients_create'),

    path('dashboard/admin/<str:facility_id>/doctors/', doctors, name='doctors'),
    path('dashboard/admin/<str:facility_id>/doctors/create/', doctors_create, name='doctors_create'),

    path('dashboard/admin/<str:facility_id>/staff/', staff, name='staff'),
    path('dashboard/admin/<str:facility_id>/staff/create/', staff_create, name='staff_create'),

    path('dashboard/admin/<str:facility_id>/appointments/', appointments, name='appointments'),
    path('dashboard/admin/<str:facility_id>/appointments/create/', appointments_create, name='appointments_create'),

    path('dashboard/admin/<str:facility_id>/services/', services, name='services'),
    path('dashboard/admin/<str:facility_id>/encounters/', encounters, name='encounters'),
]
