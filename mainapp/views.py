import json
import sys
import traceback
from datetime import datetime

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, redirect, get_object_or_404

from mailer.moreviews import send_contact_form_confirmation_email
from mailer.utils import send_custom_email
from .models import *
from facilities.models import Doctor, Appointment
from facilities.serializers import AppointmentSerializer
from django.shortcuts import reverse


@receiver(post_save, sender=Contact)
def send_contact_email(sender, instance, created, **kwargs):
    if created:
        # send_contact_form_confirmation_email(instance)
        send_custom_email('contact_form', instance, [instance.email])


def call_schedule(request):
    return render(request, template_name="schedule/call_schedule.html", context={})


def blogs(request):
    blogs_ = Blog.objects.all()
    paginator = Paginator(blogs_, 9)  # Show 9 blogs per page.

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "pages": paginator.page_range,
        "page_count": paginator.num_pages,
    }
    return render(request, template_name="blogs.html", context=context)


def single_blog(request, blog_id, slug):
    blog = get_object_or_404(Blog, id=blog_id)
    context = {
        "blog": blog,
        "related_blogs": Blog.objects.filter(topic=blog.topic)[0:2],
        "recent_blogs": Blog.objects.order_by('-id')[0:5],
        'topics': Topic.objects.all(),
        "replies": Reply.objects.filter(blog=blog, public=True),
    }
    return render(request, template_name="blog.html", context=context)


def blog_reply(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    if request.method == "POST":
        reply = Reply(
            blog=blog,
            author=request.POST.get('author'),
            comment=request.POST.get('comment'),
            email=request.POST.get('email')
        )
        reply.save()
        messages.success(request, "The reply has been posted successfully. Its undergoing preview and will "
                                  "appear if approved")
    return redirect(request.META['HTTP_REFERER'])


def doctor_search(request):
    specialist = request.GET.get('specialist', 0)
    print(specialist)
    doctors_ = Doctor.objects.filter(specialities__in=[specialist])
    print(doctors_)
    context = {
        'doctors': doctors_
    }
    return render(request, template_name="doctors/doctor-search.html", context=context)


def get_time_24(str_time):
    system_24 = {
        '1': '13',
        '2': '14',
        '3': '15',
        '4': '16',
        '12': '12'
    }

    str_time_array = str_time.strip().split(':')
    hour = str_time_array[0]
    b_array = str_time_array[1].split()
    minute = b_array[0]
    period = b_array[1]

    if period == 'AM':
        return f'{hour}:{minute}'
    else:
        hr_24 = system_24.get(hour, '')
        return f"{hr_24}:{minute}"


def single_doctor(request, doctor_id):
    appointments = Appointment.objects.filter(doctor__id=doctor_id)
    doctor_events = []
    for appointment in appointments:
        start_time = get_time_24(appointment.start_time)
        end_time = get_time_24(appointment.end_time)

        event = {
                    'id': "1",
                    'title': appointment.condition.name if getattr(appointment, 'condition') else appointment.other_condition,
                    'start': appointment.date.strftime('%Y-%m-%d') + 'T' + start_time,
                    'end':  appointment.date.strftime('%Y-%m-%d') + 'T' + end_time,
                    'url': '#',
                    'customDate': appointment.date.strftime('%a %d, %b %Y'),
                    'start_time': appointment.start_time,
                    'end_time': appointment.end_time,
                    'backgroundColor': 'blue',
                    'description': "This is a cool event",
                    'doctor': appointment.doctor.user.get_full_name(),
                    'doctorID': appointment.doctor.id,
                    'doctorURL': reverse('doctor:single-appointment',  kwargs={'appointment_id': appointment.id}),
                    'patient': appointment.patient.user.get_full_name(),
                    'patientID': appointment.patient.id,
                    'patientURL': reverse('patient:single-appointment', kwargs={'appointment_id': appointment.id}),
                }
        doctor_events.append(event)
    context = {
        'doctor': Doctor.objects.filter(id=doctor_id).first(),
        'events': json.dumps(doctor_events)
    }
    return render(request, template_name="doctors/single-doctor.html", context=context)


def page_not_found(request, exception):
    page = ''
    if request.META.get('HTTP_REFERER'):
        page = request.META['HTTP_REFERER']
    return render(request, template_name="errors/error-404.html", context={'error_page': page, 'exception': exception})


def internal_server_error(request):
    exc_type, exc_value, tb = sys.exc_info()
    traceback_data = traceback.format_tb(tb)
    error_message = ''
    if len(traceback_data) > 0:
        error_message = f'''
            <h4>Error type </h4>
            <p>{exc_value}</p>
            <h4>Traceback</h4>
            <p>{traceback_data[0]}</p>
            <p>{traceback_data[1]}</p>
        '''

    return render(request, template_name="errors/error-500.html", context={'error_message': error_message})
