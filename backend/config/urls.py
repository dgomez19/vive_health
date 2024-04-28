"""base-project backend URL Configuration
"""
from django.conf.urls import include
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/v1/security/', include('apps.security.urls')),
    path('api/v1/appointment/', include('apps.appointment.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
