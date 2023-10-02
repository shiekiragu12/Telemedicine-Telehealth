from rest_framework import routers
from django.urls import path, include
from .endpoints import ChatMessagesViewSet

router = routers.DefaultRouter()
router.register(r'messages/chat-group', ChatMessagesViewSet)

urlpatterns = [
    path('', include(router.urls))
]
