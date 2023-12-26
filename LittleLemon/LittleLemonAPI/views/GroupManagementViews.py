from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from LittleLemonAPI.permissions import IsManager
from rest_framework.response import Response
from django.contrib.auth.models import User, Group


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsManager])
def group_management_managers(request, user_id=None):
    managers = Group.objects.get(name="Manager")

    if request.method == 'GET':
        manager_names = list(managers.user_set.values_list('username', flat=True))
        return Response(manager_names, status.HTTP_200_OK)

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


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsManager])
def group_management_delivery_crew(request, user_id=None):
    delivery_crew = Group.objects.get(name="Delivery Crew")

    if request.method == 'GET':
        delivery_crew_names = list(delivery_crew.user_set.values_list('username', flat=True))
        return Response(delivery_crew_names, status.HTTP_200_OK)

    if request.method == 'POST':
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            delivery_crew.user_set.add(user)

            return Response(f'User {username} added to Delivery Crew successfully.', status.HTTP_201_CREATED)

        return Response("No username provided.", status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        if user_id is not None:
            user = get_object_or_404(User, id=user_id)
            delivery_crew.user_set.remove(user)

            return Response(f'User with id of {user_id} removed from Delivery Crew successfully.', status.HTTP_200_OK)

        return Response("No user ID provided.", status.HTTP_400_BAD_REQUEST)
