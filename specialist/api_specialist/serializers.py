from rest_framework import serializers

from .models import (
    Specialist
)


class SpecialistCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Specialist
        fields = [
            'names',
            'surnames',
            'birthdate',
            'address',
            'cell_phone',
            'document'
        ]

class SpecialistListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Specialist
        fields = [
            'uuid',
            'names',
            'surnames',
            'birthdate',
            'address',
            'cell_phone',
            'document',
            'created'
        ]