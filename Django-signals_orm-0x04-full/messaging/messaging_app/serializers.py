from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Message, Notification, MessageHistory

User = get_user_model()

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Message
        fields = ['sender', 'receiver', 'content', 'timestamp']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['user', 'message']

class MessageHistorySerializer(serializers.ModelSerializer):
    edited_by = serializers.PrimaryKeyRelatedField(required = False, read_only=True)
    class Meta:
        model = MessageHistory
        fields = ['message', 'old_content', 'edited_by', 'edited_by']
