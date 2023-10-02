from django.urls import path
from .views import *

app_name = 'patient'

urlpatterns = [
    path('dashboard/', patient_dashboard, name='dashboard'),
    path('prescriptions/', prescriptions, name='prescriptions'),
    path('prescription-orders/', prescription_orders, name='prescription-orders'),
    path('appointments/', appointments, name='appointments'),
    path('appointments/view/<str:appointment_id>/', single_appointment, name="single-appointment"),
    path('appointments/view/<str:appointment_id>/mental-form/', fill_mental_form,
         name="appointment-mental-form"),
    path('medical-reports/', medical, name='medical-reports'),
]
