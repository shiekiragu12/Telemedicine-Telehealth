from django.contrib import admin
from . import settings
from django.contrib.staticfiles.urls import static
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_URL)
