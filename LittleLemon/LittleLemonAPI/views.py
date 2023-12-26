from django.shortcuts import get_object_or_404
from .models import MenuItem
from .serializers import MenuItemSerializer
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, DjangoModelPermissions
from .permission import IsManager
from rest_framework.response import Response
from django.contrib.auth.models import User, Group


class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticatedOrReadOnly()]
        else:
            return [DjangoModelPermissions()]


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticatedOrReadOnly()]
        else:
            return [DjangoModelPermissions()]


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsManager])
def group_management_managers(request, user_id=None):
    managers = Group.objects.get(name="Manager")

    if request.method == 'GET':
        manager_names = list(managers.user_set.values_list('username', flat=True))
        return Response(manager_names, 200)

    if request.method == 'POST':
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            managers.user_set.add(user)

            return Response(f'User {username} added to Managers successfully.', status.HTTP_201_CREATED)

        return Response("No username provided.", status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        if user_id is not None:
            user = get_object_or_404(User, id=user_id)
            managers.user_set.remove(user)

            return Response(f'User with id of {user_id} removed from Managers successfully.', status.HTTP_200_OK)

        return Response("No user ID provided.", status.HTTP_400_BAD_REQUEST)
