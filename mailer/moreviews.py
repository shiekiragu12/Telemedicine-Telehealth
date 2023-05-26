from django.core.mail import get_connection, EmailMultiAlternatives
from django.template import Template, Context
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from mailer.models import SentEmail
from mailer.utils import send_email
from mainapp.models import AppConfig


def send_account_creation_email(user):
    app_config = AppConfig.objects.filter(app="main").first()
    if user is not None and app_config is not None:
        email = app_config.account_creation_email
        email_config = app_config.account_creation_emailconfig
        email_template = Template(email.body)

        email_context = Context({"user": user})

        email_html = email_template.render(email_context)

        template = render_to_string("email_template.html", context={
            'html_email': email_html,
            'subject': email.subject
        })
        text_content = strip_tags(template)

        email_text = EmailMultiAlternatives(
            email.subject,
            text_content,
            f'{email_config.title} <{email_config.email}>',
            [user.email]
        )
        email_text.attach_alternative(template, 'text/html')

        register_sent_email = SentEmail(
            user=user,
            subject=email.subject,
            body=template
        )

        send_email(email_config, [email_text], [register_sent_email])

    return {"message": "failed"}


def send_doctor_creation_email(doctor):
    app_config = AppConfig.objects.filter(app="main").first()
    if doctor is not None and app_config is not None:
        email = app_config.doctor_creation_email
        email_config = app_config.doctor_creation_emailconfig
        email_template = Template(email.body)
        email_context = Context({'doctor': doctor})

        email_html = email_template.render(email_context)

        template = render_to_string("email_template.html", context={
            'html_email': email_html,
            'subject': email.subject
        })
        text_content = strip_tags(template)

        email_text = EmailMultiAlternatives(
            email.subject,
            text_content,
            f'{email_config.title} <{email_config.email}>',
            [doctor.user.email]
        )
        email_text.attach_alternative(template, 'text/html')

        # connection.open()
        register_sent_email = SentEmail(
            user=doctor.user,
            subject=email.subject,
            body=template
        )

        send_email(email_config, [email_text], [register_sent_email])

    return {"message": "done"}


def send_doctor_authorized_email(doctor):
    app_config = AppConfig.objects.filter(app="main").first()
    if doctor is not None and app_config is not None:
        email = app_config.doctor_authorized_email
        email_config = app_config.doctor_authorized_emailconfig
        email_template = Template(email.body)
        email_context = Context({'doctor': doctor})

        email_html = email_template.render(email_context)

        template = render_to_string("email_template.html", context={
            'html_email': email_html,
            'subject': email.subject
        })
        text_content = strip_tags(template)

        email_text = EmailMultiAlternatives(
            email.subject,
            text_content,
            f'{email_config.title} <{email_config.email}>',
            [doctor.user.email]
        )
        email_text.attach_alternative(template, 'text/html')

        # connection.open()
        register_sent_email = SentEmail(
            user=doctor.user,
            subject=email.subject,
            body=template
        )

        send_email(email_config, [email_text], [register_sent_email])

    return {"message": "done"}


def send_prescription_quotation_email(quotation):
    app_config = AppConfig.objects.filter(app="main").first()
    if quotation is not None and app_config is not None:
        email = app_config.prescription_quotation_email
        email_config = app_config.prescription_quotation_emailconfig
        email_template = Template(email.body)
        email_context = Context({'quotation': quotation})

        email_html = email_template.render(email_context)

        template = render_to_string("email_template.html", context={
            'html_email': email_html,
            'subject': email.subject
        })
        text_content = strip_tags(template)

        email_text = EmailMultiAlternatives(
            email.subject,
            text_content,
            f'{email_config.title} <{email_config.email}>',
            [quotation.patient.user.email]
        )
        email_text.attach_alternative(template, 'text/html')

        # connection.open()
        register_sent_email = SentEmail(
            user=quotation.patient.user,
            subject=email.subject,
            body=template
        )

        send_email(email_config, [email_text], [register_sent_email])

    return {"message": "done"}


def send_contact_form_confirmation_email(contact):
    app_config = AppConfig.objects.filter(app="main").first()
    if contact is not None and app_config is not None:
        email = app_config.contact_form_email
        email_config = app_config.contact_form_emailconfig
        email_template = Template(email.body)
        email_context = Context({'contact': contact})

        email_html = email_template.render(email_context)

        template = render_to_string("email_template.html", context={
            'html_email': email_html,
            'subject': email.subject
        })
        text_content = strip_tags(template)

        email_text = EmailMultiAlternatives(
            email.subject,
            text_content,
            f'{email_config.title} <{email_config.email}>',
            [contact.email]
        )
        email_text.attach_alternative(template, 'text/html')

        send_email(email_config, [email_text], [])

    return {"message": "done"}
