from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

# Create your models here.
from mailer.models import EmailConfiguration, Email


class AppConfig(models.Model):
    app = models.CharField(max_length=30, blank=True, null=True, default="main", unique=True)

    account_creation_email = models.ForeignKey(Email, blank=True, null=True, on_delete=models.SET_NULL,
                                               related_name="account_creation_Email")

    account_creation_emailconfig = models.ForeignKey(EmailConfiguration, blank=True, null=True,
                                                     on_delete=models.SET_NULL,
                                                     related_name="account_creation_email_config")

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

    patient_creation_email = models.ForeignKey(Email, blank=True, null=True, on_delete=models.SET_NULL,
                                               related_name="patient_creation_email")
    patient_creation_emailconfig = models.ForeignKey(EmailConfiguration, blank=True, null=True,
                                                     on_delete=models.SET_NULL,
                                                     related_name="patient_creation_emailconfig")

    doctor_creation_email = models.ForeignKey(Email, blank=True, null=True, on_delete=models.SET_NULL,
                                              related_name="doctor_creation_email")
    doctor_creation_emailconfig = models.ForeignKey(EmailConfiguration, blank=True, null=True,
                                                    on_delete=models.SET_NULL,
                                                    related_name="doctor_creation_emailconfig")

    doctor_authorized_email = models.ForeignKey(Email, blank=True, null=True, on_delete=models.SET_NULL,
                                                related_name="doctor_authorized_email")
    doctor_authorized_emailconfig = models.ForeignKey(EmailConfiguration, blank=True, null=True,
                                                      on_delete=models.SET_NULL,
                                                      related_name="doctor_authorized_emailconfig")

    prescription_creation_email = models.ForeignKey(Email, blank=True, null=True, on_delete=models.SET_NULL,
                                                    related_name="prescription_creation_email")
    prescription_creation_emailconfig = models.ForeignKey(EmailConfiguration, blank=True, null=True,
                                                          on_delete=models.SET_NULL,
                                                          related_name="prescription_creation_emailconfig")

    prescription_quotation_email = models.ForeignKey(Email, blank=True, null=True, on_delete=models.SET_NULL,
                                                     related_name="prescription_quotation_email")
    prescription_quotation_emailconfig = models.ForeignKey(EmailConfiguration, blank=True, null=True,
                                                           on_delete=models.SET_NULL,
                                                           related_name="prescription_quotation_emailconfig")

    appointment_creation_email = models.ForeignKey(Email, blank=True, null=True, on_delete=models.SET_NULL,
                                                   related_name="appointment_creation_email")
    appointment_creation_emailconfig = models.ForeignKey(EmailConfiguration, blank=True, null=True,
                                                         on_delete=models.SET_NULL,
                                                         related_name="appointment_creation_emailconfig")

    facility_creation_email = models.ForeignKey(Email, blank=True, null=True, on_delete=models.SET_NULL,
                                                related_name="facility_creation_email")
    facility_creation_emailconfig = models.ForeignKey(EmailConfiguration, blank=True, null=True,
                                                      on_delete=models.SET_NULL,
                                                      related_name="facility_creation_emailconfig")

    facility_authorized_email = models.ForeignKey(Email, blank=True, null=True, on_delete=models.SET_NULL,
                                                  related_name="facility_authorized_email")
    facility_authorized_emailconfig = models.ForeignKey(EmailConfiguration, blank=True, null=True,
                                                        on_delete=models.SET_NULL,
                                                        related_name="facility_authorized_emailconfig")

    contact_form_email = models.ForeignKey(Email, blank=True, null=True, on_delete=models.SET_NULL,
                                           related_name="contact_form_email")
    contact_form_emailconfig = models.ForeignKey(EmailConfiguration, blank=True, null=True,
                                                 on_delete=models.SET_NULL,
                                                 related_name="contact_form_emailconfig")

    schedule_creation_email = models.ForeignKey(Email, blank=True, null=True, on_delete=models.SET_NULL,
                                                related_name="schedule_creation_email")
    schedule_creation_emailconfig = models.ForeignKey(EmailConfiguration, blank=True, null=True,
                                                      on_delete=models.SET_NULL,
                                                      related_name="schedule_creation_emailconfig")

    analytic_creation_email = models.ForeignKey(Email, blank=True, null=True, on_delete=models.SET_NULL,
                                                related_name="analytic_creation_email")
    analytic_creation_emailconfig = models.ForeignKey(EmailConfiguration, blank=True, null=True,
                                                      on_delete=models.SET_NULL,
                                                      related_name="analytic_creation_emailconfig")

    apply_creation_email = models.ForeignKey(Email, blank=True, null=True, on_delete=models.SET_NULL,
                                             related_name="apply_creation_email")
    apply_creation_emailconfig = models.ForeignKey(EmailConfiguration, blank=True, null=True,
                                                   on_delete=models.SET_NULL,
                                                   related_name="apply_creation_emailconfig")

    equip_creation_email = models.ForeignKey(Email, blank=True, null=True, on_delete=models.SET_NULL,
                                             related_name="equip_creation_email")
    equip_creation_emailconfig = models.ForeignKey(EmailConfiguration, blank=True, null=True,
                                                   on_delete=models.SET_NULL,
                                                   related_name="equip_creation_emailconfig")

    telehealth_creation_email = models.ForeignKey(Email, blank=True, null=True, on_delete=models.SET_NULL,
                                                  related_name="telehealth_creation_email")
    telehealth_creation_emailconfig = models.ForeignKey(EmailConfiguration, blank=True, null=True,
                                                        on_delete=models.SET_NULL,
                                                        related_name="telehealth_creation_emailconfig")

    demorequest_creation_email = models.ForeignKey(Email, blank=True, null=True, on_delete=models.SET_NULL,
                                                   related_name="demorequest_creation_email")
    demorequest_creation_emailconfig = models.ForeignKey(EmailConfiguration, blank=True, null=True,
                                                         on_delete=models.SET_NULL,
                                                         related_name="demorequest_creation_emailconfig")

    book_creation_email = models.ForeignKey(Email, blank=True, null=True, on_delete=models.SET_NULL,
                                            related_name="book_creation_email")
    book_creation_emailconfig = models.ForeignKey(EmailConfiguration, blank=True, null=True,
                                                  on_delete=models.SET_NULL,
                                                  related_name="book_creation_emailconfig")

    firstaid_creation_email = models.ForeignKey(Email, blank=True, null=True, on_delete=models.SET_NULL,
                                                related_name="firstaid_creation_email")
    firstaid_creation_emailconfig = models.ForeignKey(EmailConfiguration, blank=True, null=True,
                                                      on_delete=models.SET_NULL,
                                                      related_name="firstaid_creation_emailconfig")

    application_url = models.CharField(blank=True, null=True, max_length=255)
    account_creation_activated = models.BooleanField(default=True)

    def __str__(self):
        return f"Application {self.app}"


class Tag(models.Model):
    name = models.CharField(blank=False, null=False, max_length=50)

    created_on = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_on = models.DateTimeField(auto_created=True, auto_now=True)

    def __str__(self):
        return self.name


class Topic(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)

    created_on = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_on = models.DateTimeField(auto_created=True, auto_now=True)

    def __str__(self):
        return self.title


class Blog(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=500, blank=False, null=False)
    slug = models.SlugField(blank=True, null=True)
    body = models.TextField(blank=False, null=False)
    tags = models.ManyToManyField(Tag, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to="blogs/images/", blank=True, null=True)

    is_public = models.BooleanField(default=True)

    created_on = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_on = models.DateTimeField(auto_created=True, auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super(Blog, self).save(*args, **kwargs)


class Reply(models.Model):
    author = models.CharField(max_length=100)
    blog = models.ForeignKey(Blog, blank=False, null=True, on_delete=models.CASCADE)
    comment = models.TextField()
    email = models.EmailField()
    public = models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_on = models.DateTimeField(auto_created=True, auto_now=True)

    def __str__(self):
        return self.author


class Contact(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    phone_number = models.CharField(max_length=15, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    subject = models.CharField(max_length=200, blank=False, null=False)
    message = models.TextField(blank=False, null=False)
    read = models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_on = models.DateTimeField(auto_created=True, auto_now=True)

    def __str__(self):
        return f"{self.subject} - from {self.name}"
