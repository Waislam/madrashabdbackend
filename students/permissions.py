from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Group


class IsMadrashaAdmin(BasePermission):

    def has_permission(self, request, view):

        if request.user:
            # if request.user.is_superuser or request.user.is_staff:
            #     return True
            # else:
            madrasha_admin_group = Group.objects.get(name="Madrasha Admin")
            print("madrasha_admin_group", madrasha_admin_group)

            madrasha_admin = request.user.groups.filter(name=madrasha_admin_group)
            print(madrasha_admin)
            return False
        # else:
        #     return False


class IsSuperUser(BasePermission):

    def has_permission(self, request, view):

        return request.user and request.user.is_superuser


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user:
            if request.user.is_superuser:
                return True
            else:
                return obj.owner == request.user
        else:
            return False