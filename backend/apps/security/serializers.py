from rest_framework import serializers
from django.conf import settings
from .models import User


class UserListRetrieveSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    created = serializers.DateTimeField(format=settings.FORMAT_DATETIME)

    class Meta:
        model = User
        fields = ['uuid', 'created', 'username', 'first_name', 'last_name', 'email', 'role']

    def get_role(self, obj):
        return {
            'code': obj.role,
            'text': obj.get_role_display()
        }


class UserCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uuid', 'username', 'first_name', 'last_name', 'email', 'role']


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['uuid', 'first_name', 'last_name', 'email']
