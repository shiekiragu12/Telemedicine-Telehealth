from django.contrib import admin

from . import settings
from django.contrib.staticfiles.urls import static
from django.urls import path, include

urlpatterns = [
  path('admin/', admin.site.urls),
  path('', include('website.urls')),
  path('facilities/', include('facilities.urls')),
  path('shop/', include('shop.urls')),
  path('account/', include('account.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_URL) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)
