from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import MessageViewset, NotificationViewset

router = DefaultRouter()
router.register(r'messages', MessageViewset, basename='messages')
router.register(r'notifications', NotificationViewset, basename='notifications')

urlpatterns = [
    path('', include(router.urls)),
]