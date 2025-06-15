from django.urls import path, include
from .views import RegisterUser, DeleteUserView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'register', RegisterUser, basename='register')

urlpatterns = [
    path('', include(router.urls)),
    path('delete-account/', DeleteUserView.as_view(), name='delete-account'),
    path('auth/', include('rest_framework.urls')),
]