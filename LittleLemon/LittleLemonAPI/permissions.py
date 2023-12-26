from rest_framework import permissions


class IsManager(permissions.BasePermission):
    """ Custom permissions class for Managers. """

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Manager").exists()
