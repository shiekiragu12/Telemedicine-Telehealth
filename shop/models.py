from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

from mailer.utils import send_custom_email


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(default="no-default", blank=True, null=True)

    created_on = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_on = models.DateTimeField(auto_created=True, auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Category, self).save(*args, **kwargs)


class ProductType(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(default="", blank=True)

    created_on = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_on = models.DateTimeField(auto_created=True, auto_now=True)

    class Meta:
        verbose_name_plural = "Product Types"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(ProductType, self).save(*args, **kwargs)


class Product(models.Model):
    PRODUCT_STATUS = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('unapproved', 'Unapproved')
    )
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    facility = models.ForeignKey('facilities.Facility', blank=True, null=True, on_delete=models.SET_NULL)

    name = models.CharField(max_length=100, blank=False, null=False)
    slug = models.SlugField(default="", blank=True)
    brand = models.CharField(max_length=100, blank=False, null=True)
    code = models.CharField(max_length=100, blank=False, null=True)
    description = models.TextField(null=True)
    available = models.BooleanField(default=True)

    price = models.FloatField()
    price_usd = models.FloatField(default=0.0)
    image = models.ImageField(upload_to='products/images/', null=True, blank=False)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    dom = models.TextField(blank=True, null=True)
    product_type = models.ForeignKey(ProductType, blank=False, null=True, on_delete=models.SET_NULL)  # medical
    # device, allergy medicine, etc
    categories = models.ManyToManyField(Category, blank=True, related_name='categories')
    tags = models.ManyToManyField('mainapp.Tag', blank=True)
    status = models.CharField(max_length=20, blank=False, null=False, choices=PRODUCT_STATUS,
                              default='pending')

    is_live = models.BooleanField(default=True)  # To show whether the product is live or not.

    created_on = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_on = models.DateTimeField(auto_created=True, auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Product, self).save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, blank=False, null=False, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='products/images/', null=True)

    def __str__(self):
        return self.product.name


class PrescriptionOrder(models.Model):
    ORDER_STATUS = (
        ('new', 'New'),
        ('confirmed', 'Confirmed'),
        ('pending', 'Pending'),
        ('delivered', 'Delivered'),
        ('undelivered', 'Undelivered'),
    )
    patient = models.ForeignKey('facilities.Patient', blank=False, null=False, on_delete=models.CASCADE)
    facility = models.ForeignKey('facilities.Facility', blank=False, null=False, on_delete=models.CASCADE)
    prescription = models.ForeignKey('facilities.Prescription', blank=False, null=False, on_delete=models.CASCADE)
    amount = models.CharField(max_length=10, blank=False, null=True)
    notes = models.TextField()

    paid = models.BooleanField(default=False)  # To track whether the order has been paid for.

    status = models.CharField(max_length=30, blank=True, null=True, choices=ORDER_STATUS, default='new')

    created_on = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_on = models.DateTimeField(auto_created=True, auto_now=True)


@receiver(post_save, sender=PrescriptionOrder)
def send_new_quotation_creation_email(sender, instance, created, **kwargs):
    if created:
        send_custom_email('prescription_quotation', instance, [instance.patient.user.email, instance.doctor.user.email])


class Order(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    paid = models.BooleanField(default=False)
    amount = models.FloatField()

    created_on = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_on = models.DateTimeField(auto_created=True, auto_now=True)

    def __str__(self):
        return f"Order #{self.id}"


@receiver(post_save, sender=PrescriptionOrder)
def send_new_quotation_creation_email(sender, instance, created, **kwargs):
    if created:
        send_custom_email('order_creation', instance, [instance.user.email])


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=False)
    price = models.FloatField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=False, related_name='order_items')
    quantity = models.IntegerField(default=0)

    created_on = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_on = models.DateTimeField(auto_created=True, auto_now=True)

    def __str__(self):
        return f"Order - {self.order.id}"


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=False)
    amount = models.FloatField()

    paid = models.BooleanField(default=False)
    # Transaction details
    trans_ref = models.CharField(blank=True, null=True, max_length=100)
    trans_token = models.CharField(blank=True, null=True, max_length=100)
    trans_result = models.CharField(blank=True, null=True, max_length=100)
    other_trans_info = models.TextField(blank=True, null=True)
    # payment details
    payment_code = models.CharField(blank=True, null=True, max_length=100)
    amount_paid = models.FloatField(blank=True, null=True)
    other_payment_info = models.TextField(blank=True, null=True)

    created_on = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_on = models.DateTimeField(auto_created=True, auto_now=True)

    def __str__(self):
        return f"Order - {self.order.id}"
