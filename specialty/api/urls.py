from django.urls import path

from rest_framework_jwt.views import obtain_jwt_token

from .views import (
    list_specialty,
    add_specialty
)

urlpatterns = [
    path('', list_specialty, name='auth-specialty-api'),
    path('add/', add_specialty, name='auth-specialty-add-api'),
]
