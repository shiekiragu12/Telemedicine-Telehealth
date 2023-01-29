from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,  name="index"),
    # path('sign-in', views.signin, name="signin"),
    # path('sign-up', views.signup, name="signup"),
    
    # services paths
    path('services', views.service, name="service"),
    path('services/emergencies', views.emergencies, name="emergencies"),
    path('birthing-care', views.birthingcare, name="birthing-care"),
    path('cancer-care', views.cancercare, name="cancer-care"),
    path('family-medicine', views.familymedicine, name="family-medicine"), 
    path('emergency-medicine', views.emergencymedicine, name="emergency-medicine"),
    path('laboraties-center', views.laboratiescenter, name="laboraties-center"),
    path('online-referral', views.onlinereferral, name="online-referral"),
    path('first-aid', views.firstaid, name="first-aid"),
    
    # about
    path('about', views.about, name="about"),
    
    # Health in Hand
    path('health', views.health, name="health"),
    path('disease-list', views.diseaselist, name="disease-list"),
    path('health-topic', views.healthtopic, name="health-topic"),
    path('healthy-living', views.healthyliving, name="healthy-living"),
    path('location', views.location, name="location"),
    
    # solution
    path('solution', views.solution, name="solution"),
    
    
    # shop
    path('shop', views.shop, name="shop"),
    path('refill-prescription', views.prescription, name="refill-prescription"),
    path('allergy-medicine', views.allergy, name="allergy-medicine"),
    path('mobile-aid', views.mobileaid, name="mobile-aid"),
    path('medical-devices', views.medicaldevices, name="medical-devices"),
    path('prescription-medication', views.prescriptionmedication, name="prescription-medication"),
    path('nutraceuticals', views.nutraceuticals, name="nutraceuticals"),
]
