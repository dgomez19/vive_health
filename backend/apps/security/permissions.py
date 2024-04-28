from rest_framework.permissions import BasePermission
from .models import User


class IsAdministrator(BasePermission):
    """
    Validates if the authenticated user has admin role.
    """

    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and request.user.role == User.ROLE_ADMINISTRATOR
