from django.urls import path, include
from rest_framework import routers
from .views import EmailViewSet, EmailConfigViewSet


router = routers.DefaultRouter()
router.register(r'emailconfigs', EmailConfigViewSet)
router.register(r'', EmailViewSet)


urlpatterns = [
    path('', include(router.urls)),
    # router.register(r'emailconfigs', EmailConfigViewSet.as_view())
]
