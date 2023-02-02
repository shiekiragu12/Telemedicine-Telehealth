from django.db import models

# Create your models here.
from mailer.models import EmailConfiguration, Email


class AppConfig(models.Model):
    app = models.CharField(max_length=30, blank=True, null=True, default="main", unique=True)

    reset_password_email = models.ForeignKey(Email, blank=True, null=True, on_delete=models.SET_NULL,
                                             related_name="password_reset_Email")
    reset_password_emailconfig = models.ForeignKey(EmailConfiguration, blank=True, null=True, on_delete=models.SET_NULL,
                                                   related_name="password_reset_email_config")

    activate_account_email = models.ForeignKey(Email, blank=True, null=True, on_delete=models.SET_NULL,
                                               related_name="account_activation_email")
    activate_account_emailconfig = models.ForeignKey(EmailConfiguration, blank=True, null=True,
                                                     on_delete=models.SET_NULL,
                                                     related_name="account_activation_email_config")

    order_placement_email = models.ForeignKey(Email, blank=True, null=True, on_delete=models.SET_NULL,
                                              related_name="order_placement_email")
    order_placement_emailconfig = models.ForeignKey(EmailConfiguration, blank=True, null=True,
                                                    on_delete=models.SET_NULL,
                                                    related_name="order_placement_emailconfig")

    payment_made_email = models.ForeignKey(Email, blank=True, null=True, on_delete=models.SET_NULL,
                                           related_name="payment_made_email")
    payment_made_emailconfig = models.ForeignKey(EmailConfiguration, blank=True, null=True,
                                                 on_delete=models.SET_NULL, related_name="payment_made_emailconfig")

    application_url = models.CharField(blank=True, null=True, max_length=255)
    listing_activated = models.BooleanField(default=True)
    account_creation_activated = models.BooleanField(default=True)

    def __str__(self):
        return f"Application {self.app}"
