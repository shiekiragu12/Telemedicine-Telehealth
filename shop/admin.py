from django.contrib import admin
from . models import *

# Register your models here.
admin.site.register([Category, Product])
admin.site.register(PrescriptionOrder)
admin.site.register(ProductType)
admin.site.register([Order, Payment])
