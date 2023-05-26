import json

from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response

from facilities.decorators import check_facility_and_attach_it_to_request, authorized_user
from mailer.utils import send_custom_email
from mainapp.models import Blog
from .models import *


# Create your views here.

def list_product_view(request):
    products_ = Product.objects.all()
    paginator = Paginator(products_, 25)  # Show 25 products per page
    count = paginator.count

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number if int(page_number) <= count else 1)

    context = {
        "page_obj": page_obj,
        "pages": paginator.page_range,
        "page_count": paginator.num_pages,
        "total_products": count
    }

    return render(request, template_name='shop/shop.html', context=context)


def list_product_by_type(request, pk, slug):
    products_ = Product.objects.filter(product_type__id=pk)
    paginator = Paginator(products_, 25)  # Show 25 products per page
    count = paginator.count

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number if int(page_number) <= count else 1)

    context = {
        "page_obj": page_obj,
        "pages": paginator.page_range,
        "page_count": paginator.num_pages,
        "total_products": count,
        "product_type": ProductType.objects.filter(id=pk).first()
    }

    return render(request, template_name='shop/types/single-type.html', context=context)


def cart(request):
    context = {}
    return render(request, template_name='shop/cart.html', context=context)


def checkout(request):
    context = {}
    return render(request, template_name='shop/checkout.html', context=context)


@check_facility_and_attach_it_to_request
@authorized_user
def change_prescription_order_status(request, facility_id, p_id, status):
    prescription = PrescriptionOrder.objects.filter(id=p_id).first()
    if prescription:
        prescription.status = status
        prescription.save()
        messages.success(request, 'The prescription order status has been changed successfully')
    else:
        messages.error(request, 'The prescription order was not found on the server')
    return redirect(request.META['HTTP_REFERER'])


@api_view(['POST'])
def place_order(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        items = json.loads(request.data['data'])
        total = 0
        order_items = []
        for item in items:
            product = Product.objects.filter(id=item['id']).first()
            if product is not None:
                total += product.price * item["qty"]
                order_items.append(
                    OrderItem(product=product, price=product.price, quantity=item["qty"]))
        order = Order.objects.create(user=request.user, amount=total)
        order.save()
        for order_item in order_items:
            order_item.order = order

        OrderItem.objects.bulk_create(order_items)

        send_custom_email('order_creation', order, [request.user.email])

        return Response({"message": "success", "order": "created"})
    messages.error(request, "An error occurred while placing the order")
    return redirect('checkout')
