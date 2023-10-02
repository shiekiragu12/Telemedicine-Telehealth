from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from facilities.decorators import check_facility_and_attach_it_to_request
from facilities.utils import is_not_blank_or_empty
from mainapp.models import Tag
from .models import *
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from facilities.models import *
from shop.models import Product, PrescriptionOrder, ProductType, Category, Order


# Create your views here.


@login_required(login_url='signin')
@check_facility_and_attach_it_to_request
def pharmacy_dashboard(request, facility_id):
    products_ = Product.objects.filter(facility=request.facility)
    pres_orders = PrescriptionOrder.objects.filter(facility=request.facility)
    shared_prescriptions_ = SharedPrescription.objects.filter(facility=request.facility)

    context = {
        "total_products": products_.count(),
        "total_pending_products": products_.filter(status="pending").count(),
        "total_approved_products": products_.filter(status="approved").count(),
        "total_unapproved_products": products_.filter(status="unapproved").count(),
        # "total_prescriptions": request.facility.shared_prescriptions.all().count(),
        'total_shared_prescriptions': shared_prescriptions_.count(),
        "total_prescriptions": pres_orders.count(),
        "total_confirmed_prescriptions": pres_orders.filter(status="confirmed").count(),
        "total_pending_prescriptions": pres_orders.filter(status="pending").count(),
        "total_delivered_prescriptions": pres_orders.filter(status="delivered").count(),
        "total_undelivered_prescriptions": pres_orders.filter(status="undelivered").count(),
    }
    return render(request, template_name='pharmacy-dashboard/pages/index.html', context=context)


@login_required(login_url='signin')
@check_facility_and_attach_it_to_request
def edit_facility(request, facility_id):
    context = {
        'facility_types': FacilityType.objects.all(),
        'counties': County.objects.all(),
        'specialities': Speciality.objects.all(),
        'options': [
            {"label": "Pharmacy", "value": 'pharmacy'},
            {"label": "Clinic", "value": 'clinic'},
            {"label": "Nutraceutical", "value": 'nutraceutical'},
        ]
    }
    return render(request, template_name='pharmacy-dashboard/pages/editfacility.html', context=context)


@login_required(login_url='signin')
@check_facility_and_attach_it_to_request
def upload_product(request, facility_id):
    context = {
        'tags': Tag.objects.all(),
        'product_types': ProductType.objects.all(),
        'product_categories': Category.objects.all()
    }
    return render(request, template_name='pharmacy-dashboard/pages/upload-product.html', context=context)


@login_required(login_url='signin')
@check_facility_and_attach_it_to_request
def create_pharmacy(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        pharma_name = request.POST.get('pharma_name')
        location = request.POST.get('location')
        licence = request.POST.get('licence')
        email = request.POST.get('email')
        alternative_email = request.POST.get('alternative_email')
        number = request.POST.get('number')
        alternative_number = request.POST.get('alternative_number')
        created_on = request.POST.get('created_on')
        attach = request.FILES.get('image')
        subject = 'Form submission received'
        body = 'Thank you for submitting the form your form is currently under review'
        email = EmailMessage(subject, body, to=[request.POST['email']])
        email.send()

        existingpharmacy = Pharmacy.objects.filter(
            pharma_name=pharma_name).exists()

        # user = User.objects.order_by('-pk')[0]

        pharmacy = Pharmacy(first_name=first_name, last_name=last_name, pharma_name=pharma_name,
                            location=location, licence=licence, email=email, alternative_email=alternative_email,
                            number=number, alternative_number=alternative_number, date_created=created_on,
                            attach=attach)

        pharmacy.save()
        messages.success(
            request, 'Pharmacy created successfully wait for approval')
        return redirect('index')

    return render(request, template_name='pharmacy/verification-form.html', context={})


@login_required(login_url='signin')
@check_facility_and_attach_it_to_request
def send_order_email(request, facility_id):
    # Get the user's email address from the request
    email = request.POST.get('email')

    # Send the email
    send_mail(
        'Order Confirmation',
        'Your order has been placed. Thank you!',
        'your-default-from-email',
        [email],
        fail_silently=False,
    )
    context = {}
    context['patients'] = Patient.objects.all()
    # Render a template to display a confirmation message to the user
    return render(request, template_name='pharmacy-dashboard/pages/prescription-orders.html', context=context)


@login_required(login_url='signin')
@check_facility_and_attach_it_to_request
def modal_view(request, facility_id):
    return render(request, template_name='pharmacy-dashboard/pages/product_modal.html', context={})


@login_required(login_url='signin')
@check_facility_and_attach_it_to_request
def modal_view_redirect(request, facility_id):
    return redirect('pharmacetical:upload-product')


@login_required(login_url='signin')
@check_facility_and_attach_it_to_request
def live_product(request, facility_id):
    context = {'live_products': Product.objects.filter(facility__id=request.facility.id).filter(status='approved').filter(is_live=True)}
    return render(request, template_name='pharmacy-dashboard/pages/live-product.html', context=context)


@login_required(login_url='signin')
@check_facility_and_attach_it_to_request
def pending_product(request, facility_id):
    context = {'pending_products': Product.objects.filter(facility__id=request.facility.id).filter(status='pending')}
    return render(request, template_name='pharmacy-dashboard/pages/pending-product.html', context=context)


@login_required(login_url='signin')
@check_facility_and_attach_it_to_request
def unapproved_product(request, facility_id):
    products_ = Product.objects.filter(facility__id=request.facility.id).filter(status='unapproved')
    context = {'unapproved_products': products_}
    return render(request, template_name='pharmacy-dashboard/pages/unapproved-products.html', context=context)


@login_required(login_url='signin')
@check_facility_and_attach_it_to_request
def approved_product(request, facility_id):
    context = {'approved_products': Product.objects.filter(facility__id=request.facility.id).filter(status='approved')}
    return render(request, template_name='pharmacy-dashboard/pages/approved-products.html', context=context)


@check_facility_and_attach_it_to_request
def update_product(request, facility_id, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {
        "product": product,
        'tags': Tag.objects.all(),
        'product_types': ProductType.objects.all(),
        'product_categories': Category.objects.all()
    }
    return render(request, template_name='pharmacy-dashboard/pages/product-detail.html', context=context)


@login_required(login_url='signin')
@check_facility_and_attach_it_to_request
def shared_prescriptions(request, facility_id):
    context = {'prescriptions': SharedPrescription.objects.filter(facility=request.facility)}
    return render(request, template_name='pharmacy-dashboard/pages/shared_prescriptions.html', context=context)


@login_required(login_url='signin')
@check_facility_and_attach_it_to_request
def prescription_orders(request, facility_id):
    context = {'prescriptions': PrescriptionOrder.objects.filter(facility=request.facility)}
    return render(request, template_name='pharmacy-dashboard/pages/prescription-orders.html', context=context)


@login_required(login_url='signin')
@check_facility_and_attach_it_to_request
def pending_orders(request, facility_id):
    context = {'prescriptions': PrescriptionOrder.objects.filter(facility=request.facility).filter(status='pending')}
    return render(request, template_name='pharmacy-dashboard/pages/pending-orders.html', context=context)


@login_required(login_url='signin')
@check_facility_and_attach_it_to_request
def confirmed_orders(request, facility_id):
    context = {'prescriptions': PrescriptionOrder.objects.filter(facility=request.facility).filter(status='confirmed')}
    return render(request, template_name='pharmacy-dashboard/pages/confirmed.html', context=context)


@login_required(login_url='signin')
@check_facility_and_attach_it_to_request
def delivered_orders(request, facility_id):
    context = {'prescriptions': PrescriptionOrder.objects.filter(facility=request.facility).filter(
        status='delivered')}
    return render(request, template_name='pharmacy-dashboard/pages/delivered-orders.html', context=context)


@login_required(login_url='signin')
@check_facility_and_attach_it_to_request
def undelivered_orders(request, facility_id):
    context = {'prescriptions': PrescriptionOrder.objects.filter(facility=request.facility).filter(
        status='undelivered')}
    return render(request, template_name='pharmacy-dashboard/pages/undelivered-orders.html', context=context)


@login_required(login_url='signin')
@check_facility_and_attach_it_to_request
def pharmacy_report(request, facility_id):
    return render(request, template_name='pharmacy-dashboard/pages/pharmacy-report.html', context={})


@login_required(login_url='signin')
@check_facility_and_attach_it_to_request
def create_product(request, facility_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        brand = request.POST.get('brand')
        price = request.POST.get('price')
        discount = request.POST.get('discount')
        dom = request.POST.get('dom')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        code = request.POST.get('code')

        product = Product(name=name, discount=discount, brand=brand, price=price,
                          dom=dom, description=description, image=image, code=code)

        product.save()
        messages.success(request, 'Product uploaded successfully')
        return redirect('pharmacetical:upload-product')

    return render(request, template_name='pharmacy-dashboard/pages/pharmacy-index.html', context={})


@login_required(login_url='signin')
@check_facility_and_attach_it_to_request
def product_orders(request, facility_id):

    orders_ = Order.objects.get_queryset().order_by('id')
    orders_2 = Order.objects.filter(order_items__product__facility_id=facility_id).order_by('id')

    search = request.GET.get('search', None)
    ordering = request.GET.get('ordering', None)
    limit = request.GET.get('limit')  # Show 25 results per page.

    if is_not_blank_or_empty(search):
        orders_2 = orders_2.filter(
            Q(user__first_name__icontains=search) | Q(user__last_name__icontains=search) |
            Q(user__username__icontains=search) |
            Q(user__email__icontains=search))

    paginator = Paginator(orders_2,
                          limit if is_not_blank_or_empty(limit) else 25)  # Show 25 facilities per page.

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number if int(page_number) <= paginator.num_pages else 1)

    context = {
        "page_obj": page_obj,
        "pages": paginator.page_range,
        "page_count": paginator.num_pages,
        "paginator_count": paginator.count,
        "total_orders": orders_.count(),
    }
    return render(request, template_name='pharmacy-dashboard/pages/product-orders.html', context=context)


@login_required(login_url='signin')
@check_facility_and_attach_it_to_request
def single_order(request, facility_id, order_id):
    context = {
        'order': Order.objects.filter(id=order_id).first()
    }
    return render(request, template_name='pharmacy-dashboard/pages/single-order.html', context=context)
