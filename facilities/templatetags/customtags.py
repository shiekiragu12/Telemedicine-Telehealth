from django import template
from django.urls import reverse

register = template.Library()


@register.filter
def reverse_url(url_name, facility_id, facility_slug):
    return reverse(url_name, args=[facility_id, facility_slug])
