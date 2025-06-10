from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """Model to create/display the user"""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'bio', 'phone_number', 'password', 'confirm_password'
        ]
        read_only_fields = ['user_id']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        return user


class ConversationSerializer(serializers.ModelSerializer):
    """Create conversation serializer"""
    participants = serializers.SlugRelatedField(
        many=True,
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    """Create Message Serializer"""
    username = serializers.CharField(source='sender.username', read_only=True)
    first_name = serializers.CharField(source='sender.first_name', read_only=True)
    last_name = serializers.CharField(source='sender.last_name', read_only=True)

    class Meta:
        model = Message
        fields = [
            'message_id', 'username', 'first_name', 'last_name',
            'conversation', 'message_body', 'sent_at'
        ]
        read_only_fields = [
            'message_id', 'sent_at', 'username', 'first_name', 'last_name'
        ]

