from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.index, name="index"),

    # services paths
    path('services/emergencies', views.emergencies, name="emergencies"),
    path('services/birthing-care', views.birthingcare, name="birthing-care"),
    path('services/mental-health', views.mental_health, name="mental-health"),
    path('services/cancer-care', views.cancercare, name="cancer-care"),
    path('services/family-medicine', views.familymedicine, name="family-medicine"),
    path('services/emergency-medicine', views.emergencymedicine, name="emergency-medicine"),
    path('services/laboratories-center', views.laboratiescenter, name="laboratories-center"),
    path('services/online-referral', views.onlinereferral, name="online-referral"),
    path('services/first-aid', views.firstaid, name="first-aid"),

    # about
    path('about', views.about, name="about"),

    # Health in Hand
    path('health', views.health, name="health"),
    path('disease-list', views.diseaselist, name="disease-list"),
    path('health-topic', views.healthtopic, name="health-topic"),
    path('healthy-living', views.healthyliving, name="healthy-living"),
    path('location', views.location, name="location"),
    path('teams', views.teams, name="teams"),
    path('project', views.project, name="project"),
    path('project-details', views.projectdetails, name="project-details"),
    path('faq', views.faq, name="faq"),
    path('appointment', views.appointment, name="appointment"),
    path('testimonials', views.testimonials, name="testimonials"),
    path('how-it-works', views.howitworks, name="how-it-works"),

    # solution
    path('solution', views.solution, name="solution"),
    path('blog', views.blog, name="blog"),
    path('contact', views.contact, name="contact"),
    path('symptom-checker', views.symptom_checker, name="symptom_checker"),

    # shop
    path('shop', views.shop, name="shop"),
    path('prescription-medication', views.prescriptionmedication, name="prescription-medication"),
    # Other product types are stored in db to be dynamic

    # solution
    path('solution/emergency-medical-response', views.emergency, name="emergency"),
    path('solution/analytic-solutions', views.analytic, name="analytic"),
    path('solution/healthcare-equipment-financing', views.equip, name="equip"),
    path('solution/healthcare-services-financing', views.healthcare, name="healthcare"),
    path('solution/telehealth-facilities-hosting', views.telehealth, name="telehealth"),
    path('solution/IT-medicare', views.medicare, name="medicare"),

    path('solution/schedule', views.schedule, name="schedule"),
    path('solution/apply', views.apply, name="apply"),
    path('solution/apply_equip', views.applyEquip, name="apply_equip"),
    path('solutin/analytic_action', views.analyticAction, name="analytic_action"),
    path('solution/apply_tele', views.applyTele, name="apply_tele"),

    path('request_form', views.request_form, name='request_form'),
    path('book', views.book, name='book'),
    path('first_aid', views.first_aid, name='first_aid'),

    #  Terms & Conditions
    # path('terms-and-conditions/user-policy', name, name='user-policy'),
    path('terms-and-conditions', views.terms_conditions, name="terms-conditions"),
    path('terms-and-conditions/privacy-policy', views.privacy_policy, name="privacy-policy"),
    path('terms-and-conditions/user-policy', views.user_policy, name="user-policy"),
    path('terms-and-conditions/practitioner-policy', views.practitioner_policy, name="practitioner-policy"),
]
