from django import template
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
import json
from datetime import date
from django.utils import timezone

from django.urls import reverse
from django.utils.text import slugify

from facilities.models import Condition, Doctor, FacilitySpeciality, Illness, County, Constituency, Facility
from facilities.serializers import ConditionSerializer, FacilityTypeSerializer, ServiceSerializer, \
    ServiceCategorySerializer, CountySerializer, ConstituencySerializer
from shop.models import ProductType, Category, Product
from mailer.serializers import EmailConfigSerializer, EmailSerializer
from shop.serializers import CategorySerializer, ProductTypeSerializer
from superadmin.models import Media
from mainapp.models import Tag, Topic, Contact

import pycountry

from website.models import Firstaid, DemoRequest, Telehealth, Book, Schedule, Analytic, Apply, Equip

register = template.Library()


@register.filter
def to_json(obj, target):
    serializer = None
    if target == 'condition':
        serializer = ConditionSerializer(obj, many=False)
    if target == 'emailconfig':
        serializer = EmailConfigSerializer(obj, many=False)
    if target == 'email':
        serializer = EmailSerializer(obj, many=False)
    if target == 'facility_type':
        serializer = FacilityTypeSerializer(obj, many=False)
    if target == 'service_category':
        serializer = ServiceCategorySerializer(obj, many=False)
    if target == 'product_category':
        serializer = CategorySerializer(obj, many=False)
    if target == 'product_type':
        serializer = ProductTypeSerializer(obj, many=False)
    if target == 'service':
        serializer = ServiceSerializer(obj, many=False)
    if target == 'county':
        serializer = CountySerializer(obj, many=False)
    if target == 'constituency':
        serializer = ConstituencySerializer(obj, many=False)
    return json.dumps(serializer.data if serializer else serializer)


@register.filter
def get_full_url(url_name):
    return reverse(url_name)


@register.filter
def match_paths(path, view_name):
    if path == reverse(view_name):
        return True
    return False


@register.filter
def get_first_letter(text):
    if text:
        return text[0:1]
    return 'N/A'


@register.filter
def calculate_age(date_of_birth):
    today = timezone.now().date()
    if date_of_birth:
        age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
        return age
    return "N/A"


@register.filter
def get_range(count):
    return range(0, count)


@register.filter
def custom_slugify(text):
    return slugify(text)


@register.filter
def product_types(text):
    return ProductType.objects.all()


@register.filter
def tags(text):
    return Tag.objects.all()


@register.filter
def categories(text):
    return Category.objects.all()


@register.filter
def statuses(text):
    PRODUCT_STATUS = [
        {"value": "pending", "label": "Pending"},
        {"value": "approved", "label": "Approved"},
        {"value": "unapproved", "label": "Unapproved"},
    ]
    return PRODUCT_STATUS


@register.filter
def conditions(text):
    return Condition.objects.all()


@register.filter
def illness(text):
    return Illness.objects.all().order_by('name')


@register.filter
def doctors(text):
    return Doctor.objects.all()


@register.filter
def specialities(text):
    return FacilitySpeciality.objects.all()


image_extensions = ["ai", "bmp", "eps", "gif", "ico", "jpeg", "jpg", "png", "ps", "psd", "svg", "tif", "tiff", "webp"]
video_extensions = ["mp4", "avi", "mov"]
document_extensions = ["doc", "docx", "ppt", "pptx", "pdf"]
excel_extensions = ["xls", "xlsx"]


@register.filter
def get_media(media_type):
    media_ = Media.objects.all()

    if media_type == 'images':
        files = []
        for file in media_:
            extension = file.file.name.split('.')[1]
            if extension in image_extensions:
                files.append(file)
        return files
    return []


@register.filter
def update_page_param(path, page):
    parsed_url = urlparse(path)
    query_params = dict(parse_qsl(parsed_url.query))
    query_params['page'] = page
    new_query_string = urlencode(query_params)
    new_path = parsed_url.path + '?' + new_query_string if new_query_string else parsed_url.path
    return new_path


@register.filter
def counties(text):
    return County.objects.all()


@register.filter
def constituencies(text):
    return Constituency.objects.all()


@register.filter
def topics(text):
    return Topic.objects.all()


@register.filter(name='country_codes')
def country_codes(some_country):
    codes = []
    # for country in pycountry.countries:
    #     phone_code = '+' + str(int(country.numeric))
    #     codes.append(phone_code)
    codes.append('+254')
    return codes


@register.filter
def get_notification_count(facility_kind):
    return Facility.objects.filter(facility_kind=facility_kind).filter(authorized=False).count()


@register.filter
def get_notification_count_products(products_str):
    return Product.objects.filter(status='pending').count()


@register.filter
def get_unread_count(model):
    if model == 'contact-form':
        return Contact.objects.filter(read=False).count()
    if model == 'book-form':
        return Book.objects.filter(read=False).count()
    if model == 'schedule-form':
        return Schedule.objects.filter(read=False).count()
    if model == 'analytic-form':
        return Analytic.objects.filter(read=False).count()
    if model == 'apply-form':
        return Apply.objects.filter(read=False).count()
    if model == 'equip-form':
        return Equip.objects.filter(read=False).count()
    if model == 'telehealth-form':
        return Telehealth.objects.filter(read=False).count()
    if model == 'demo-form':
        return DemoRequest.objects.filter(read=False).count()
    if model == 'first-aid-form':
        return Firstaid.objects.filter(read=False).count()
    else:
        return 0


@register.filter
def is_page_active(view_name, path):
    if view_name:
        return reverse(view_name) == path
    return False


def make_link(label, view_name, icon=None, unread_count_name=None, path="", children=[]):
    return {
        'label': label,
        'view_name': view_name,
        'icon': icon,
        'unread_count': unread_count_name,
        'active': reverse(view_name) == path if view_name else False,
        'children': children,
    }


@register.filter
def get_contact_links(links):
    links = [make_link('Contact Form', 'super-admin-contact-form', 'contact_page', 'contact-form'),
             make_link('Booking Appointments', 'super-admin-book-form', 'book_online', 'book-form'),
             make_link('Analytic Solution', 'super-admin-analytic-form', 'on_device_training', 'analytic-form'),
             make_link('Equip Financing', 'super-admin-equip-form', 'biotech', 'equip-form'),
             make_link('Schedule', 'super-admin-schedule-form', 'biotech', 'schedule-form'),
             make_link('Apply', 'super-admin-apply-form', 'spa', 'apply-form'),
             make_link('Facility Hosting', 'super-admin-telehealth-form', 'local_hospital', 'telehealth-form'),
             make_link('Demo Requests', 'super-admin-demo-requests-form', 'devices', 'demo-form'),
             make_link('Emergency Response', 'super-admin-first-aid-form', 'contact_emergency', 'first-aid-form')]

    return links


@register.filter
def get_navbar_links(group_name, path):
    if group_name == 'services':
        links = [
            make_link('Emergencies', 'emergencies', None, None, path),
            make_link('Emergency Medicine', 'emergency-medicine', None, None, path),
            make_link('Mental Health', 'mental-health', None, None, path),
            make_link('Family Medicine', 'family-medicine', None, None, path),
            make_link('Cancer Care', 'cancer-care', None, None, path),
            make_link('Laboratory Centers', 'laboratories-center', None, None, path),
            make_link('Birthing Care', 'birthing-care', None, None, path),
            make_link('Online Referrals', 'online-referral', None, None, path),
            make_link('Patient Safety', 'first-aid', None, None, path),
        ]
        return links
    if group_name == 'solutions':
        links = [
            make_link('Scheduler', 'call_schedule', None, None, path),
            # make_link('Symptom Checker', 'symptom_checker', None, None, path),
            make_link('Analytic Solutions', 'analytic', None, None, path),
            make_link('Healthcare services financing', 'healthcare', None, None, path),
            make_link('Healthcare equip financing', 'equip', None, None, path),
            make_link('Med E-commerce', 'shop', None, None, path),
            make_link('IT Medicare solutions', 'medicare', None, None, path),
            make_link('Telehealth facilities Hosting', 'telehealth', None, None, path),
            # make_link('Emergency medical response', 'analytic', None, None, path),
        ]
        return links
    if group_name == 'health-in-hand':
        links = [
            make_link('Team', 'teams', None, None, path),
            make_link('Health information', None, None, None, path, [
                make_link('Diseases Conditions A-Z', 'disease-list', None, None, path),
                make_link('General Health Topics', 'health-topic', None, None, path),
                make_link('Healthy living and lifestyle', 'healthy-living', None, None, path),
                make_link(' Medical facilities and location', 'facilities', None, None, path),
            ]),
            # make_link('Projects', 'projects', None, None, path),
            make_link('FAQ', 'faq', None, None, path),
            make_link('Appointment', 'appointment', None, None, path),
            make_link('Testimonials', 'testimonials', None, None, path),
            make_link('How it works', 'how-it-works', None, None, path),
            make_link('Terms & Conditions', 'terms-conditions', None, None, path),
            make_link('Privacy Policy', 'privacy-policy', None, None, path),
            make_link('User Policy', 'user-policy', None, None, path),
            make_link('Practitioner Policy', 'practitioner-policy', None, None, path),
        ]
        return links

    return []


@register.filter
def multiply(a, b):
    return a * b


@register.filter
def get_doctor_specialties(specs):
    return " | ".join([spec.name for spec in specs])


@register.filter
def get_date(date_obj):
    return date_obj.strftime('%Y-%m-%d')
