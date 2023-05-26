from django.urls import path
from .views import *

app_name = 'doctor'

urlpatterns = [
    path('dashboard/', doctor_dashboard, name="dashboard"),
    path('prescriptions/', prescriptions, name="prescriptions"),
    path('appointments/', appointments, name="appointments"),
    path('appointments/view/<str:appointment_id>/', single_appointment, name="single-appointment"),
    path('medical-reports/', medical_reports, name="medical-reports"),
    path('lab-orders/', lab_orders, name="lab-orders"),
    path('consultation-notes/', consultation_notes, name="consultation-notes"),
    path('text-consultation/', text_consultations, name="text-consultation"),
    path('video-consultation/', video_consultations, name="video-consultation"),
]
