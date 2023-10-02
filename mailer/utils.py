from django.core.mail import get_connection
from django.core.mail import EmailMultiAlternatives
from django.template import Template, Context
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .helperfuncs import get_instance_mail_settings
from .models import SentEmail


def send_email(email_config, emails, sent_mails = []):
    connection = get_connection(
        host=email_config.host,
        port=email_config.port,
        username=email_config.email,
        password=email_config.password,
        from_email=f'{email_config.title} <{email_config.email}>',
    )

    try:
        connection.open()
        connection.send_messages(emails)
        connection.close()
        for email in sent_mails:
            email.sent = True
        SentEmail.objects.bulk_create(sent_mails)
        return {
            "message": "success"
        }
    except Exception as e:
        SentEmail.objects.bulk_create(sent_mails)
        return {
            "message": "failed"
        }


def send_custom_email(instance_name, instance, email_receivers):
    """
    :param instance_name: The instance that we are targeting to email ie account_creation, company_creation
    :param instance: The model instance or object targeted, can be a custom object
    :param email_receivers: A list of receivers of the email ie  ['info@gmail.com']
    :return: Object containing message: 'success' or 'failed' or 'email configuration not found' - Indicating settings
    for emails not properly done
    """
    mail_settings = get_instance_mail_settings(instance_name)
    email = mail_settings['email']
    email_config = mail_settings['email_config']

    if email_config:
        email_template = Template(email.body)
        email_context = Context({instance_name: instance})

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
            email_receivers
        )
        email_text.attach_alternative(template, 'text/html')
        sent_mails = []
        for receiver in email_receivers:
            sent_mail = SentEmail(
                receiver=receiver,
                subject=email.subject,
                body=template,
                sent=False
            )
            sent_mails.append(sent_mail)
        # print("Starting to send email")
        result = send_email(email_config, [email_text], sent_mails)
        # print('Result: ', result)

        return result
    return {
        "message": "Email configuration not found"
    }
