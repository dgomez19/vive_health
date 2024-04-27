from django.urls import path

from .views import (
    list_specialist,
    add_specialist
)

urlpatterns = [
    path('', list_specialist, name='auth-list-specialist-api'),
    path('add/', add_specialist, name='auth-list-specialist-api'),
]
