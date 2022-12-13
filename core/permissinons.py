from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Group
from accounts.models import Madrasha


class IsMadrashaUser(BasePermission):

    def has_permission(self, request, view):
        Madrasha.objects.get()
        if request.user:

            print(request.user)
            if request.user.is_superuser or request.user.is_staff:
                return True
            else:
                madrasha_admin_group = Group.objects.get(name="Madrasha Admin")
                print("madrasha_admin_group", madrasha_admin_group)

                madrasha_admin = request.user.groups.filter(name=madrasha_admin_group)
                print(madrasha_admin)
                return True
        else:
            return False