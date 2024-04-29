from rest_framework import filters

from rest_framework import status

from rest_framework.views import Response

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView
)

from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    Specialist,
    Specialty,
    Patient,
    Appointment
)

from .serializers import (
    SpecialistSerializer,
    PatientCreateSerializer,
    PatientListSerializer,
    SpecialtySerializer,
    AppointmentCreateSerializer,
    AppointmentListSerializer,
    SpecialistAvailableTimesSerializer
)

from apps.core.mixins import ProtectedForeignKeyDeleteMixin

from config.pagination import Pagination


class PatientListCreate(ListCreateAPIView):
    queryset = Patient.objects.all()
    lookup_field = "uuid"
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, filters.SearchFilter)
    pagination_class = Pagination

    def get_serializer_class(self):
        if self.request and self.request.method == 'POST':
            return PatientCreateSerializer
        return PatientListSerializer


class PatientRetrieveUpdateDestroyAPIView(ProtectedForeignKeyDeleteMixin, RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientListSerializer
    lookup_field = "uuid"
    ordering = ('-id')
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('names', 'surnames', 'document')


class SpecialistListCreate(ListCreateAPIView):
    queryset = Specialist.objects.all()
    serializer_class = SpecialistSerializer
    pagination_class = Pagination
    lookup_field = "uuid"
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('names', 'surnames', 'document')


class SpecialistRetrieveUpdateDestroyAPIView(ProtectedForeignKeyDeleteMixin, RetrieveUpdateDestroyAPIView):
    queryset = Specialist.objects.all()
    serializer_class = SpecialistSerializer
    lookup_field = "uuid"
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('names', 'surnames', 'document')


class SpecialtyListCreate(ListCreateAPIView):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
    lookup_field = "uuid"
    pagination_class = Pagination
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('name',)


class SpecialtyRetrieveUpdateDestroyAPIView(ProtectedForeignKeyDeleteMixin,
                                            RetrieveUpdateDestroyAPIView):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
    lookup_field = "uuid"
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)


class AppointmentListCreate(ListCreateAPIView):
    queryset = Appointment.objects.all()
    lookup_field = "uuid"
    pagination_class = Pagination
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = [
        'patient__uuid',
        'specialist__uuid',
        'specialty__uuid'
    ]

    ordering = ('-patient', )

    def get_serializer_class(self):
        if self.request and self.request.method == 'POST':
            return AppointmentCreateSerializer
        return AppointmentListSerializer


class AvailableTimesListAPIView(ListAPIView):
    def get(self, request):
        if request.GET.get('specialist'):
            specialists = Specialist.objects.filter(uuid=request.GET.get('specialist'))
        else:
            specialists = Specialist.objects.all()

        specialist_serializer = SpecialistAvailableTimesSerializer(specialists, many=True, context={'request': request})
        return Response(specialist_serializer.data, status=status.HTTP_200_OK)
