from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name='super-admin'),

    # Settings
    path('settings/', settings, name='super-admin-settings'),

    # Users
    path('users/', users, name='super-admin-users'),
    path('users/change/<str:user_id>/', single_user, name='super-admin-users-single'),

    path('doctors/', doctors, name='super-admin-doctors'),
    path('doctors/change/<str:doctor_id>/', single_doctor, name='super-admin-doctors-single'),
    path('doctors/change/status/<str:doctor_id>/<str:status>/', change_doctor_status,
         name='super-admin-doctors-change-status'),

    path('staff/', staff, name='super-admin-staff'),
    path('staff/change/<str:staff_id>/', single_staff, name='super-admin-staff-single'),

    path('patients/', patients, name='super-admin-patients'),
    path('patients/change/<str:patient_id>/', single_patient, name='super-admin-patients-single'),

    # Emails and email settings
    path('emails/', emails, name='super-admin-emails'),
    path('emails/configurations/', emailconfigs, name='super-admin-emailconfigs'),
    path('emails/email-template-variables/', email_variables, name='super-admin-email-template-variables'),

    # Location - counties & constituencies
    path('counties/', counties, name='super-admin-counties'),
    path('constituencies/', constituencies, name='super-admin-constituencies'),

    # Facilities
    path('facilities/', facilities, name='super-admin-facilities'),
    path('facilities/change/<str:facility_id>/', single_facility, name='super-admin-facilities-single'),

    path('facilities/type/hospitals/', hospitals, name='super-admin-hospitals'),
    path('facilities/type/clinics', clinics, name='super-admin-clinics'),
    path('facilities/type/pharmacies/', pharmacies, name='super-admin-pharmacies'),
    path('facilities/type/nutraceuticals/', nutraceuticals, name='super-admin-nutraceuticals'),

    path('facilities/update/<str:facility_id>/<str:status>/', change_facility_status,
         name='super-admin-facilities-update'),

    path('facilities/types/', facility_types, name='super-admin-facility_types'),
    path('facilities/upload/', upload_medical_facilities, name="super-admin-upload-facilities"),

    path('conditions/', conditions, name='super-admin-conditions'),
    path('conditions/upload/', upload_conditions, name="super-admin-conditions-upload"),

    path('illness/', illness_page, name='super-admin-illness'),
    path('illness/upload/', upload_illness, name='super-admin-illness-upload'),

    path('specialities/', specialities, name='super-admin-specialities'),
    path('specialities/upload/', upload_specialities, name='super-admin-specialities-upload'),

    path('services-categories/', service_categories, name='super-admin-service_categories'),
    path('services/', services, name='super-admin-services'),
    path('appointments/', appointments, name='super-admin-appointments'),
    path('patient-medical-data/', encounters, name='super-admin-encounters'),

    # Shop
    path('products/', products, name='super-admin-products'),
    path('products/change/<str:product_id>/', single_product, name='super-admin-products-single'),
    path('products/update/status/<str:product_id>/<str:status>/', change_product_status, name='super-admin-products'
                                                                                              '-status'),
    path('product-categories/', product_categories, name='super-admin-product_categories'),
    path('product-types/', product_types, name='super-admin-product_types'),
    path('orders/', orders, name='super-admin-orders'),
    path('orders/details/<str:order_id>/', single_order, name='super-admin-orders-single'),

    # Blogs
    path('blogs/', blogs, name='super-admin-blogs'),
    path('blogs/new-blog/', new_blog, name='super-admin-new-blog'),
    path('blogs/update/<str:blog_id>/', update_blog, name='super-admin-blog-update'),
    path('blogs/tags/', tags, name='super-admin-blog-tags'),

    path('media', media, name='super-admin-media'),

    # Contact
    path('contact', contact_form, name="super-admin-contact-form"),
    path('appointment/bookings/', book_form, name="super-admin-book-form"),
    path('appointment/schedule/', schedule_form, name="super-admin-schedule-form"),

    path('appointment/analytic/', analytic_form, name="super-admin-analytic-form"),
    path('appointment/apply/', apply_form, name="super-admin-apply-form"),
    path('appointment/equip/', equip_form, name="super-admin-equip-form"),
    path('appointment/telehealth/', telehealth_form, name="super-admin-telehealth-form"),
    path('appointment/demo-requests/', top_button_form, name="super-admin-demo-requests-form"),
    path('appointment/first_aid/', first_aid_form, name="super-admin-first-aid-form"),
]
