from rest_framework.views import APIView
from django.conf import settings

from rest_framework.response import Response

from rest_framework.decorators import api_view, authentication_classes

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import Specialist

from rest_framework import status

from .serializers import (
    SpecialistCreateSerializer,
    SpecialistListSerializer
)

@api_view(http_method_names=["GET"])
def list_specialist(request):
    try:
        specialists = Specialist.build_filters(request.GET)
        specialists_serializer = SpecialistListSerializer(specialists, many=True)
        return Response(specialists_serializer.data, status=status.HTTP_200_OK)
    except Exception as error:
        return Response(str(error), status=status.HTTP_400_BAD_REQUEST)

@api_view(http_method_names=["POST"])
def add_specialist(request):
    try:
        specialist_serializer = SpecialistCreateSerializer(data=request.data)

        if specialist_serializer.is_valid():
            specialist_serializer.save()
        else:
            return Response(specialist_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)
    except Exception as error:
        return Response(str(error), status=status.HTTP_400_BAD_REQUEST)
