from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response


from rest_framework import viewsets
from .serializers import RegistrationSerializer

User = get_user_model()

class RegisterUser(viewsets.ModelViewSet):
    serializer_class = RegistrationSerializer
    queryset = User.objects.all()
    http_method_names = ['post']


class DeleteUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response("User deleted", status = status.HTTP_204_NO_CONTENT)

