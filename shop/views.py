import json
import webbrowser

import requests
import xmltodict
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from facilities.decorators import check_facility_and_attach_it_to_request, authorized_user
from facilities.utils import is_not_blank_or_empty
from mailer.utils import send_custom_email
from .models import *
from django.shortcuts import reverse
from django.views.decorators.csrf import csrf_exempt


# @receiver(post_save, sender=Order)
# def redirect_to_payment_page(sender, instance, created, **kwargs):
#     if created:
#         return initiate_transaction(instance)


def list_product_view(request):
    products_ = Product.objects.all().order_by('id')

    product_type = request.GET.get('product_type', None)
    category = request.GET.get('category', None)
    tags_ = request.GET.get('tags', None)

    search = request.GET.get('search', None)
    ordering = request.GET.get('ordering', None)

    if is_not_blank_or_empty(product_type):
        products_ = products_.filter(product_type=product_type)

    if is_not_blank_or_empty(category):
        products_ = products_.filter(categories__id=int(category))

    if is_not_blank_or_empty(tags_):
        products_ = products_.filter(tags__id__in=[int(tags_)])

    if is_not_blank_or_empty(search):
        products_ = products_.filter(
            Q(name__icontains=search) | Q(code__icontains=search) | Q(description__icontains=search) | Q(
                dom__icontains=search))

    if is_not_blank_or_empty(ordering):
        products_ = products_.order_by(ordering)

    paginator = Paginator(products_, 25)  # Show 25 products per page
    # count = paginator.count

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "pages": paginator.page_range,
        "page_count": paginator.num_pages,
        "total_products": 0
    }

    return render(request, template_name='shop/shop.html', context=context)


def single_product(request, pk, slug):
    product = get_object_or_404(Product, id=pk)
    related_products = Product.objects.filter(product_type__id=product.product_type.id).exclude(id=pk)
    context = {
        "product": product,
        "related_products": related_products
    }
    return render(request, template_name="shop/single-product.html", context=context)


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


@login_required(login_url="signin")
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
        res = initiate_transaction(order)

        if res['message'] == "success":
            webbrowser.open(res['payment_url'])
        return Response({"message": "success", "order": "created", "payment_url": res["payment_url"]})
    messages.error(request, "An error occurred while placing the order")
    return redirect('checkout')


def initiate_transaction(order):

    payment = Payment.objects.create(order=order, amount=order.amount)
    payment.save()
    date = order.created_on.strftime('%Y/%m/%d %H:%M')

    message = ""
    payment_url = ""
    callback_url = settings.DPO_CALLBACK_URL

    try:
        url = settings.DPO_LIVE_ENDPOINT
        xml = f"""
                <?xml version="1.0" encoding="utf-8"?>
                <API3G>
                    <CompanyToken>{settings.DPO_COMPANY_TOKEN}</CompanyToken>
                    <Request>createToken</Request>
                    <Transaction>
                        <PaymentAmount>{order.amount}</PaymentAmount>
                        <PaymentCurrency>{settings.DPO_PAYMENT_CURRENCY}</PaymentCurrency>
                        <CompanyRef>{settings.DPO_COMPANY_REF}</CompanyRef>
                        <RedirectURL>{settings.DPO_REDIRECT_URL}</RedirectURL>
                        <BackURL>{callback_url}</BackURL>
                        <CompanyRefUnique>0</CompanyRefUnique>
                        <PTL>30</PTL>
                    </Transaction>
                    <Services>
                        <Service>
                            <ServiceType>{settings.DPO_SERVICE_TYPE}</ServiceType>
                            <ServiceDescription>Purchase of medical supplies</ServiceDescription>
                            <ServiceDate>{date}</ServiceDate>
                        </Service>
                    </Services>
                </API3G>
            """
        # print(xml)
        headers = {'Content-Type': 'application/xml'}
        r = requests.post(url, data=xml, headers=headers)
        xml_response = r.text

        json_ = xmltodict.parse(xml_response)

        api3g = getProperty(json_, 'API3G')
        trans_token = getProperty(api3g, 'TransToken')
        payment.trans_ref = getProperty(api3g, 'TransRef')
        payment.trans_token = trans_token
        payment.trans_result = getProperty(api3g, 'Result')
        payment.other_trans_info = json.dumps(json_)
        payment.save()
        payment_url = settings.DPO_PAYMENT_URL.format(trans_token)
        message = "success"
    except requests.exceptions.RequestException as e:
        message = "failed"
    return {
        "message": message,
        "payment_url": payment_url
    }


@csrf_exempt
def process_dpo_payment(request):
    print("Reached")
    print(request.body)
    json_ = xmltodict.parse(request.body)
    payment = getProperty(json_, 'API3G')
    trans_token = getProperty(payment, 'TransactionToken')
    payment_amount = getProperty(payment, 'TransactionAmount')
    payment = Payment.objects.filter(trans_token=trans_token).first()
    if payment:
        payment.amount_paid = payment_amount
        payment.other_payment_info = json.dumps(json_)
        payment.paid = True
        payment.save()
    return HttpResponse(status=200, content="OK")


# def dpo_charge_token(trans_token):
#     url = settings.DPO_LIVE_ENDPOINT
#     xml = f"""
#             <?xml version="1.0" encoding="utf-8"?>
#             <API3G>
#               <CompanyToken>{settings.DPO_COMPANY_TOKEN}</CompanyToken>
#               <Request>chargeTokenAuth</Request>
#               <TransactionToken>{trans_token}</TransactionToken>
#             </API3G>
#         """
#     # print(xml)
#     headers = {'Content-Type': 'application/xml'}
#     r = requests.post(url, data=xml, headers=headers)
#     xml_response = r.text
#     print(xml_response)
#
#     json_ = xmltodict.parse(xml_response)
#     return "Done"


# def dpo_initiate_mobile_payment(trans_token):
#     url = settings.DPO_LIVE_ENDPOINT
#     xml = f"""
#             <?xml version="1.0" encoding="UTF-8"?>
#             <API3G>
#               <CompanyToken>{settings.DPO_COMPANY_TOKEN}</CompanyToken>
#               <Request>ChargeTokenMobile</Request>
#               <TransactionToken>{trans_token}</TransactionToken>
#               <PhoneNumber>254706522473</PhoneNumber>
#               <MNO>mpesa</MNO>
#               <MNOcountry>kenya</MNOcountry>
#             </API3G>
#         """
#     # print(xml)
#     headers = {'Content-Type': 'application/xml'}
#     r = requests.post(url, data=xml, headers=headers)
#     xml_response = r.text
#
#     return "Done"


def getProperty(json_, prop):
    if prop in json_:
        return json_[prop]

#
# @csrf_exempt
# def process_sasa_payment(request):
#     # print("payment reached")
#     if request.method == "POST":
#         body = request.body
#         data = json.loads(body)
#         # print("Payment data:", data)
#         payment = Payment.objects.create(
#             merchant_request_id=data["MerchantRequestID"],
#             checkout_request_id=data["CheckoutRequestID"],
#             result_code=data["ResultCode"],
#             result_desc=data["ResultDesc"],
#             trans_amount=data["TransAmount"],
#             bill_ref_number=data["BillRefNumber"],
#             transaction_date_ts=data["TransactionDate"],
#             customer_mobile=data["CustomerMobile"],
#         )
#         payment.save()
#
#         pending_transaction = PendingTransaction.objects.filter(checkout_request_id=payment.checkout_request_id).first()
#         if pending_transaction is not None:
#             pending_transaction.payment = payment
#             pending_transaction.paid = True
#             pending_transaction.save()
#
#             current_date = datetime.today()
#             user = pending_transaction.user
#
#             membership = MemberShip.objects.create(
#                 user=user,
#                 plan=pending_transaction.plan,
#                 started_on=current_date,
#                 to_end_on=current_date + timedelta(days=31),
#                 is_active=True,
#                 payment=payment
#             )
#             user.profile.plan = pending_transaction.plan
#             user.profile.is_public = True
#             user.profile.save()
#             payment.user = user
#             payment.save()
#
#             membership.save()
#
#     return JsonResponse({
#         "message": "Payment processed successfully by Kilimani Hot",
#         "data": data
#     })
