"""Views for the user, conversation and messages"""
from rest_framework import viewsets
from rest_framework import permissions

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from .serializers import UserSerializer, ConversationSerializer, MessageSerializer
from .models import User, Message, Conversation
from .permisssions import IsConversationParticipant, IsSelfOrReadOnly, IsSenderOrReadOnly


class UserView(viewsets.ModelViewSet):
    """Allow creating, retrieving, updating and deleting a user"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSelfOrReadOnly,]

    def get_queryset(self):
        user_id = self.kwargs.get('pk')
        if user_id:
            return User.objects.filter(pk = user_id)
        return User.objects.filter(pk = self.request.user.pk)
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.AllowAny()]        
        return [permissions.IsAuthenticated(), IsSelfOrReadOnly()]
    
    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            raise PermissionDenied("Logged in users cannot create new account. Log out first.")
        return super().create(request, *args, **kwargs)


class MessageView(viewsets.ModelViewSet):
    """Allow creating, updating and deleting user messages."""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsSenderOrReadOnly]

    def get_queryset(self):
        conversation = self.kwargs.get('conversation_pk')
        print("ID is: ", conversation)
        print("conversation = ", get_object_or_404(Conversation, pk=conversation))
        return Message.objects.filter(converstation_id = conversation)

    def perform_create(self, serializer):
        return serializer.save(sender = self.request.user)
    
    def perform_update(self, serializer):
        if serializer.instance.sender != self.request.user:
            raise PermissionDenied("You cannot edit messages you didn't send.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.sender != self.request.user:
            raise PermissionDenied("You cannot delete messages you didn't send.")
        instance.delete()


class ConversationView(viewsets.ModelViewSet):
    """Allow users to create, update and delete conversations they are part of."""
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsConversationParticipant]

    def perform_create(self, serializer):
        """Save the conversation and automatically add
        the requesting user as a participant."""
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
    
    def get_queryset(self):
        """Only return conversations where the request user is a participant."""
        return Conversation.objects.filter(participants = self.request.user)
    
