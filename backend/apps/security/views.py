from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView, Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters, exceptions
from rest_framework_jwt.settings import api_settings
from config.pagination import Pagination
from .models import User
from .serializers import UserListRetrieveSerializer, UserCreateUpdateSerializer, ProfileSerializer
from config.mixins import ProtectedForeignKeyDeleteMixin
from apps.security.permissions import IsAdministrator
from .utils import validate_password
import traceback
from rest_framework_jwt.views import ObtainJSONWebToken


class LoginUserGetJWT(ObtainJSONWebToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code != status.HTTP_200_OK:
            return Response({'error': 'Credenciales incorrectas'}, status=status.HTTP_400_BAD_REQUEST)

        return response


class LoginUserAPIView(GenericAPIView):

    queryset = User.objects.all()
    lookup_field = 'uuid'
    permission_classes = (IsAdministrator,)

    def post(self, request, uuid):

        user = self.get_object()

        if request.user.pk == user.pk:
            raise exceptions.ValidationError(detail='No es posible acceder a la misma sesión.')

        payload = api_settings.JWT_PAYLOAD_HANDLER(user)
        token = api_settings.JWT_ENCODE_HANDLER(payload)
        response_data = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER(token, user, request)

        return Response(response_data)


class UserListCreateAPIView(ListCreateAPIView):
    """
    It is in charge of listing and creating the users, it supports the methods:
    GET, POST
    """
    queryset = User.objects.all()
    serializer_class = UserListRetrieveSerializer
    lookup_field = 'uuid'
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend)
    search_fields = ('username', 'first_name', 'last_name', 'email')
    filter_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-id')
    pagination_class = Pagination

    def get_serializer_class(self):
        if self.request and self.request.method == 'POST':
            return UserCreateUpdateSerializer
        return UserListRetrieveSerializer

    def get_queryset(self):
        return User.objects.all()

    def perform_create(self, serializer):
        serializer.save()


class UserRetrieveUpdateDestroyAPIView(ProtectedForeignKeyDeleteMixin, RetrieveUpdateDestroyAPIView):
    """
    It is responsible for viewing, editing and deleting users, supports the methods:
    GET, PUT, DELETE
    """
    queryset = User.objects.all()
    serializer_class = UserListRetrieveSerializer
    lookup_field = 'uuid'

    def get_serializer_class(self):
        if self.request and self.request.method == 'PUT':
            return UserCreateUpdateSerializer
        return UserListRetrieveSerializer

    def get_queryset(self):
        return User.objects.all()


class RolesUserListAPIView(APIView):
    """
    It is in charge of listing the user roles
    """

    def get(self, request):
        list_items = []

        for item in User.CHOICE_ROLES:
            list_items.append({
                'code': item[0],
                'text': item[1],
            })
        return Response(list_items, status=status.HTTP_200_OK)


class ProfileView(APIView):
    """
    It is in charge of updating the user profile, it supports the methods:
    GET, PUT
    """

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = ProfileSerializer(request.user, data=request.data)
        new_password = request.data.get('new_password', None)
        current_password = request.data.get('current_password', None)

        if serializer.is_valid():
            serializer.save()
        else:
            return Response({'detail': 'Petición no válida.', 'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        if new_password:
            if not validate_password(new_password):
                raise exceptions.ValidationError(detail="La contraseña no cumple con el formato establecido.")

            if request.user.check_password(current_password):
                try:
                    request.user.set_password(new_password)
                    request.user.save()
                except Exception:
                    return Response({"detail": "Error al actualizar el password."},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({"detail": "Las contraseñas no coinciden."},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Perfil actualizado correctamente.."},
                        status=status.HTTP_200_OK)


class UserGeneratePasswordAPIView(APIView):
    """
    It is in charge of generating a new password for the user and sending it by mail. It supports the GET method.
    """

    permission_classes = (IsAuthenticated, IsAdministrator)

    def get(self, request, uuid):
        try:
            kwargs = {'uuid': uuid}
            user = User.objects.get(**kwargs)
            user.generate_new_password()
            return Response({'detail': 'Clave de usuario generada correctamente.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail': 'El usuario no existe.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            traceback.print_exc()
            return Response({'detail': 'Ocurrió un error al generar la clave del usuario.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserForgotPasswordAPIView(APIView):
    """
    Validate that the email exists, if so
    send a new password to the mail, supports the POST method
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request):

        if not request.data.get('email'):
            return Response({"detail": "Debe ingresar un correo electrónico."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=request.data.get('email'))
        except User.DoesNotExist:
            return Response({"detail": "Los datos ingresados no corresponden a la información registrada"},
                            status=status.HTTP_400_BAD_REQUEST)

        user.generate_new_password()
        return Response(["Clave de usuario generada correctamente."], status=status.HTTP_200_OK)
