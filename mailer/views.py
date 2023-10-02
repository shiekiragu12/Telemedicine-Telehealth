from django.core.mail import EmailMultiAlternatives, get_connection
from django.template import Template, Context
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter

from shop.models import Order
from shop.serializers import OrderSerializer
from .models import EmailConfiguration, Email, SentEmail
from mainapp.models import AppConfig
from .serializers import EmailSerializer, EmailConfigSerializer

from account.tokens import account_activation_token
from mainapp.extraclasses import StandardResultsSetPagination
from .utils import send_email


def sendepasswordresetmail(user, token):
    app_config = AppConfig.objects.filter(app="main").first()
    if user is not None and app_config is not None:
        email = app_config.reset_password_email
        email_config = app_config.reset_password_emailconfig

        email_template = Template(email.body)
        email_context = Context({'first_name': user.first_name,
                                 'last_name': user.last_name,
                                 'email': user.email,
                                 'full_name': f"{user.first_name} {user.last_name}",
                                 'token': token,
                                 })

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

        # connection.open()
        register_sent_email = SentEmail(
            receiver=user.email,
            subject=email.subject,
            body=template,
            sent=False
        )

        send_email(email_config, [email_text], [register_sent_email])

    return {"message": "failed"}


class EmailViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows emails to be viewed or edited.
    """
    queryset = Email.objects.all()
    serializer_class = EmailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    pagination_class = StandardResultsSetPagination

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['created_by__id']
    search_fields = ["subject", "body", "description"]


class EmailConfigViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows email configurations to be viewed or edited.
    """
    queryset = EmailConfiguration.objects.all()
    serializer_class = EmailConfigSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    pagination_class = StandardResultsSetPagination

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['created_by__id']
    search_fields = ["title", "email"]