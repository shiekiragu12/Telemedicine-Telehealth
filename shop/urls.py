from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', list_product_view, name='shop'),
    path('product-types/<str:pk>/<str:slug>/', list_product_by_type, name='shop-product-type'),
    path('cart/', cart, name='cart'),

    path('checkout/', checkout, name='checkout'),
    path('checkout/orders/make/', place_order, name="place_order"),

    path('change/prescription/order/status/<str:facility_id>/<str:p_id>/<str:status>/',
         change_prescription_order_status, name='change-prescription-order-status')
]
