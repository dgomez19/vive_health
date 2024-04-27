from rest_framework.views import APIView
from django.conf import settings

from rest_framework.response import Response

from rest_framework.decorators import api_view, authentication_classes

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import Specialty

from rest_framework import status

from .serializers import (
    SpecialtyCreateSerializer,
    SpecialtyListSerializer
)


@api_view(http_method_names=["GET"])
def list_specialty(request):
    try:
        specialties = Specialty.objects.all()
        specialties_serializer = SpecialtyListSerializer(specialties, many=True)
        return Response(specialties_serializer.data, status=status.HTTP_200_OK)
    except Exception as error:
        return Response(str(error), status=status.HTTP_400_BAD_REQUEST)

@api_view(http_method_names=["POST"])
def add_specialty(request):
    try:
        specialty_serializer = SpecialtyCreateSerializer(data=request.data)

        if specialty_serializer.is_valid():
            specialty_serializer.save()
        else:
            return Response(specialty_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)
    except Exception as error:
        return Response(str(error), status=status.HTTP_400_BAD_REQUEST)
