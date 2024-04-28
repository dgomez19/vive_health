from django.urls import path
from . import views

urlpatterns = [
    path(
        'patient/',
        views.PatientListCreate.as_view(),
        name='patient-specialist-api'
    ),
    path(
        "patient/<uuid:uuid>/",
        views.PatientRetrieveUpdateDestroyAPIView.as_view(),
        name="patient-specialist-api",
    ),

    path(
        'specialist/',
        views.SpecialistListCreate.as_view(),
        name='appointment-specialist-api'
    ),
    path(
        "specialist/<uuid:uuid>/",
        views.SpecialistRetrieveUpdateDestroyAPIView.as_view(),
        name="appointment-specialist-api",
    ),

    path(
        'specialty/',
        views.SpecialtyListCreate.as_view(),
        name='appointment-specialty-api'
    ),
    path(
        "specialty/<uuid:uuid>/",
        views.SpecialtyRetrieveUpdateDestroyAPIView.as_view(),
        name="appointment-specialty-api",
    ),

    path(
        '',
        views.AppointmentListCreate.as_view(),
        name='appointment-api'
    ),

    path(
        'available-times/',
        views.AvailableTimesListAPIView.as_view(),
        name='appointment-available-times-api'
    ),
]
