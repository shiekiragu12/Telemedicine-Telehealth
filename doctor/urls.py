from django.urls import path
from .views import *

app_name = 'doctor'

urlpatterns = [
    path('add-qualification/', add_qualification, name="add-qualification"),
    path('dashboard/', doctor_dashboard, name="dashboard"),
    path('prescriptions/', prescriptions, name="prescriptions"),
    path('appointments/', appointments, name="appointments"),
    path('appointments/view/<str:appointment_id>/', single_appointment, name="single-appointment"),
    # Forms
    path('appointments/view/<str:appointment_id>/lab-form', fill_lab_test_form, name="lab-form"),
    path('appointments/view/<str:appointment_id>/mental-form', fill_mental_form, name="mental-form"),
    path('appointments/view/<str:appointment_id>/doctor-notes-form', fill_doctor_notes_form, name="doctor-notes-form"),
    # End forms
    path('medical-reports/', medical_reports, name="medical-reports"),
    path('lab-orders/', lab_orders, name="lab-orders"),
    path('consultation-notes/', consultation_notes, name="consultation-notes"),
    path('text-consultation/', text_consultations, name="text-consultation"),
    path('video-consultation/', video_consultations, name="video-consultation"),

    path('appointments/create/', create_appointment, name="create-appointment")
]
