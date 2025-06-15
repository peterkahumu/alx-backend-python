from django.urls import path, include
from .views import RegisterUser

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'register', RegisterUser, basename='register')

urlpatterns = [
    path('', include(router.urls))   
]