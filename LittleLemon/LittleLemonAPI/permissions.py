from rest_framework import permissions


class IsManager(permissions.BasePermission):
    """ Custom permissions class for Managers. """

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Manager").exists()

    @staticmethod
    def check(request):
        return request.user.groups.filter(name="Manager").exists()


class IsCustomer(permissions.BasePermission):
    """ Custom permissions class for Customers. """

    def has_permission(self, request, view):
        return not request.user.groups.exists()

    @staticmethod
    def check(request):
        return not request.user.groups.exists()


class IsDeliveryCrew(permissions.BasePermission):
    """ Custom permissions class for Delivery Crew. """

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Delivery Crew").exists()

    @staticmethod
    def check(request):
        return request.user.groups.filter(name="Delivery Crew").exists()
