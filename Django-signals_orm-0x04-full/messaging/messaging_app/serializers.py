from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Message, Notification

User = get_user_model()

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Message
        fields = ['sender', 'receiver', 'content', 'timestamp']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['user', 'message']