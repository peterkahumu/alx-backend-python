from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework import viewsets
from .serializers import RegistrationSerializer

User = get_user_model()

class RegisterUser(viewsets.ModelViewSet):
    serializer_class = RegistrationSerializer
    queryset = User.objects.all()
    http_method_names = ['post']
