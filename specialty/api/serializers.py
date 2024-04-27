from rest_framework import serializers

from .models import (
    Specialty
)


class SpecialtyCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Specialty
        fields = [
            'name'
        ]

class SpecialtyListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Specialty
        fields = [
            'uuid',
            'name',
            'created'
        ]