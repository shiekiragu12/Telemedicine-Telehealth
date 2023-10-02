from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import ChatMessage
from .serializers import ChatMessageSerializer


class ChatMessagesViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.get_queryset().select_related('sender').order_by('id')
    serializer_class = ChatMessageSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # search_fields = []
    filterset_fields = ['id', 'appointment__id']

