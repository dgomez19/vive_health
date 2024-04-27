from rest_framework.views import APIView
from django.conf import settings

from rest_framework.response import Response

from rest_framework.decorators import api_view, authentication_classes

from rest_framework_jwt.authentication import JSONWebTokenAuthentication


@authentication_classes([JSONWebTokenAuthentication,])
@api_view(http_method_names=["POST"])
def daniel(request):
    print("daniel")
    return Response({"message": "Email sent successfully"}, status=200)

