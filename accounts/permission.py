from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model
from .models import Madrasha

user = get_user_model()


class MadrashaAdminPermission(BasePermission):
    """permission class for MadrashaAdmin, developer superuser and dev staff"""
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            user_madrasha_id = request.user.madrasha.madrasha_id
            user = request.user
            # if user.exits()
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'MADRASHA-ADMIN' or request.user.is_superuser or request.user.is_staff:
            return True
        return False