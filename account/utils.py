from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def sendsignupemail(email, context):
    template = render_to_string('email/welcome email.html',
                                context=context
                                )
    text_content = strip_tags(template)
    email_text = EmailMultiAlternatives(
        'Welcome to Resq',
        text_content,
        'Resq <web@resq.co.ke>',
        [email],
    )
    email_text.attach_alternative(template, 'text/html')

    try:
        res = email_text.send(fail_silently=False)
        if res == 1:
            print('EMAIL SENT')
        else:
            print('Sending the email failed')
    except Exception as e:
        print(e)
