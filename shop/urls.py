from django.urls import path
from .views import *

urlpatterns = [
    path('', list_product_view, name='shop'),
    path('product/<str:pk>/<str:slug>/', single_product, name='single-product'),
    path('product-types/<str:pk>/<str:slug>/', list_product_by_type, name='shop-product-type'),
    path('cart/', cart, name='cart'),

    path('checkout/', checkout, name='checkout'),
    path('checkout/orders/make/', place_order, name="place_order"),
    path('checkout/orders/payments/process', process_dpo_payment, name='process-payment'),

    path('change/prescription/order/status/<str:facility_id>/<str:p_id>/<str:status>/',
         change_prescription_order_status, name='change-prescription-order-status')
]
