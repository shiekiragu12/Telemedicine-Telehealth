from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

from mailer.moreviews import send_prescription_quotation_email


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(default="")

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
    brand = models.CharField(max_length=100, blank=False, null=True)
    code = models.CharField(max_length=100, blank=False, null=True)
    description = models.TextField(null=True)
    available = models.BooleanField(default=True)

    price = models.FloatField()
    image = models.FileField(upload_to='products/images/', null=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    dom = models.TextField(blank=True, null=True)
    product_type = models.ForeignKey(ProductType, blank=True, null=True, on_delete=models.SET_NULL)  # medical
    # device, allergy medicine, etc
    category = models.ManyToManyField(Category, blank=True)
    tags = models.ManyToManyField('mainapp.Tag', blank=True)
    status = models.CharField(max_length=20, blank=False, null=False, choices=PRODUCT_STATUS,
                              default='pending')

    is_live = models.BooleanField(default=True)  # To show whether the product is live or not.

    created_on = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_on = models.DateTimeField(auto_created=True, auto_now=True)

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     # self.created_by = self.request.user
    #     return super(Product, self).save(*args, **kwargs)


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
        send_prescription_quotation_email(instance)


class Order(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    paid = models.BooleanField(default=False)
    amount = models.FloatField()

    created_on = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_on = models.DateTimeField(auto_created=True, auto_now=True)

    def __str__(self):
        return self.user.username


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

    created_on = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_on = models.DateTimeField(auto_created=True, auto_now=True)

    def __str__(self):
        return f"Order - {self.order.id}"
