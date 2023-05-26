from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

app_name = 'pharmaceutical'
urlpatterns = [
    path('create_pharmacy', create_pharmacy, name='create_pharmacy'),

    path('<str:facility_id>/edit/', edit_facility, name='edit_facility'),

    path('<str:facility_id>/dashboard/', pharmacy_dashboard, name='dashboard'),
    path('<str:facility_id>/upload-product/', upload_product, name='upload-product'),
    path('<str:facility_id>/create-product/', create_product, name='create-product'),
    path('<str:facility_id>/live-product/', live_product, name='live-product'),
    path('<str:facility_id>/pending-product/', pending_product, name='pending-product'),
    path('<str:facility_id>/approved-product/', approved_product, name='approved-product'),
    path('<str:facility_id>/unapproved-product/', unapproved_product, name='unapproved-product'),
    path('<str:facility_id>/products/detail/<str:product_id>/', update_product, name='update-product'),

    path('<str:facility_id>/products/orders/', product_orders, name='product-orders'),
    path('<str:facility_id>/products/orders/<str:order_id>/', single_order, name='product-orders-single'),

    path('<str:facility_id>/shared-prescriptions/', shared_prescriptions, name='shared-prescriptions'),
    path('<str:facility_id>/pending-orders/', pending_orders, name='pending-orders'),
    path('<str:facility_id>/delivers-orders/', delivered_orders, name='delivered-orders'),
    path('<str:facility_id>/undelivered-orders/', undelivered_orders, name='undelivered-orders'),
    path('<str:facility_id>/confirmed-orders/', confirmed_orders, name='confirmed-orders'),

    path('<str:facility_id>/pharmacy-report/', pharmacy_report, name='pharmacy-report'),
    path('<str:facility_id>/send_order_email/', send_order_email, name='send_order_email'),
    path('<str:facility_id>/prescription-orders/', prescription_orders, name='prescription-orders'),
    path('<str:facility_id>/prescription-orders/', prescription_orders, name='prescription-orders'),
    path('product-modal-redirect/', modal_view_redirect, name='product-modal-redirect'),
]
