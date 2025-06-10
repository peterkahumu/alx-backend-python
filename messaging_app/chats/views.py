"""Views for the user, conversation and messages"""
from rest_framework import viewsets
from rest_framework import permissions

from django.core.exceptions import PermissionDenied

from .serializers import UserSerializer, ConversationSerializer, MessageSerializer
from .models import User, Message, Conversation


class UserView(viewsets.ModelViewSet):
    """Allow creating, retrieving, updating and deleting a user"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return User.objects.filter(user_id = self.request.user.user_id)
        return User.objects.none()

    def get_object(self):
        """Restrict editing, deleting to creator."""
        obj = super().get_object()
        if self.request.method in ['PUT', 'PATCH', 'DELETE'] and obj != self.request.user:
            raise PermissionDenied("You cannot edit another users information.")
        return obj
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            raise PermissionDenied("Logged in users cannot create new account. Log out first.")
        return super().create(request, *args, **kwargs)