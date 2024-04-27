from rest_framework import serializers

from .models import (
    Appointment,
    Specialist
)


class AppointmentCreateSerializer(serializers.ModelSerializer):

    specialist = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=Specialist.objects.all()
    )

    class Meta:
        model = Appointment
        fields = [
            'uuid',
            'specialist'
        ]

class AppointmentListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = [
            'uuid',
            'specialist',
            'created'
        ]