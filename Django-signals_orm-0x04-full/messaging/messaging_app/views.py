from django.shortcuts import render

from rest_framework import viewsets
from .serializers import MessageSerializer, NotificationSerializer, MessageHistorySerializer
from .models import Message, Notification, MessageHistory

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


class MessageHistoryViewset(viewsets.ModelViewSet):
    serializer_class = MessageHistorySerializer
    queryset = MessageHistory.objects.all()
    permission_classes = []
    authentication_classes = []

