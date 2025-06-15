from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import MessageViewset, NotificationViewset, MessageHistoryViewset

router = DefaultRouter()
router.register(r'messages', MessageViewset, basename='messages')
router.register(r'notifications', NotificationViewset, basename='notifications')
router.register(r'history', MessageHistoryViewset, basename='message_history')

urlpatterns = [
    path('', include(router.urls)),
]