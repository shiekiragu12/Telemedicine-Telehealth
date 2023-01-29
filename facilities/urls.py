from django.urls import path
from .views import *

urlpatterns = [
    path('<str:facility_id>/', dashboard, name='dashboard'),
    # path('login/', dashboard, name='login'),
    # path('register/', dashboard, name='register'),
    path('<str:facility_id>/patients/', patients, name='patients'),
    path('<str:facility_id>/doctors/', doctors, name='doctors'),
    path('<str:facility_id>/staff/', staff, name='staff'),
    path('<str:facility_id>/appointment/', appointments, name='appointments'),
    path('<str:facility_id>/services/', services, name='services'),
    path('<str:facility_id>/encounters/', encounters, name='encounters'),
]
