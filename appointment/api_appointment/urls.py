from django.urls import path

from .views import (
    list_appointment,
    add_appointment
)

urlpatterns = [
    path('', list_appointment, name='auth-list-appointment-api'),
    path('add/', add_appointment, name='auth-list-appointment-api'),
]
