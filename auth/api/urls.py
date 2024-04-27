from django.urls import path

from rest_framework_jwt.views import obtain_jwt_token

from .views import (
    daniel,
)

urlpatterns = [
    path('login/', obtain_jwt_token, name='auth-login-api'),
    path('daniel/', daniel, name='auth-daniel-api'),
]
