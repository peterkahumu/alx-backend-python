from django.shortcuts import render

from rest_framework import viewsets
from .serializers import MessageSerializer, NotificationSerializer
from .models import Message, Notification

class MessageViewset(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    permission_classes = []
    authentication_classes = []

class NotificationViewset(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    permission_classes = []
    authentication_classes = []


