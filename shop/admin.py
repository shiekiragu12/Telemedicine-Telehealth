from django.contrib import admin
from . models import *
from .utils import ReadOnlyInlineFormSet


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ['name', 'status', 'is_live']
    list_editable = ['status', 'is_live']
    list_filter = ['product_type', 'status', 'is_live', 'categories', 'tags']
    search_fields = ['name', 'description', 'brand']


class PaymentInline(admin.StackedInline):
    model = Payment
    formset = ReadOnlyInlineFormSet
    exclude = ['amount', 'trans_result', 'other_trans_info', 'payment_code', 'other_payment_info']
    readonly_fields = ['paid', 'trans_token', 'trans_ref', 'amount_paid']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    formset = ReadOnlyInlineFormSet
    extra = 0

    readonly_fields = ['product_name', 'product_price', 'quantity', 'product_type']
    exclude = ['product', 'price']

    @staticmethod
    def product_name(instance):
        return instance.product.name

    @staticmethod
    def product_price(instance):
        return instance.product.price

    @staticmethod
    def product_type(instance):
        return instance.product.product_type.name


class OrderAdmin(admin.ModelAdmin):
    inlines = [PaymentInline, OrderItemInline]
    list_display = ['user', 'amount', 'paid', 'items_count']
    exclude = ['user']
    readonly_fields = ['amount', 'paid', 'customer_name', 'email', 'username', 'phone_number']

    list_filter = ['paid']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__email']

    @staticmethod
    def items_count(instance):
        return len(instance.order_items.all())

    @staticmethod
    def customer_name(instance):
        return instance.user.get_full_name()

    @staticmethod
    def username(instance):
        return instance.user.username

    @staticmethod
    def email(instance):
        return instance.user.email

    @staticmethod
    def phone_number(instance):
        return instance.user.profile.phone_number if hasattr(instance, 'profile') else "NO PROFILE"


admin.site.register(Category)
admin.site.register(ProductImage)
admin.site.register(Product, ProductAdmin)
admin.site.register(PrescriptionOrder)
admin.site.register(ProductType)
admin.site.register(Order, OrderAdmin)
admin.site.register([Payment])
