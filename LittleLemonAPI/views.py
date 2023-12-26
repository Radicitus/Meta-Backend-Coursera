from .models import MenuItem
from .serializers import MenuItemSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, DjangoModelPermissions


class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticatedOrReadOnly()]
        else:
            return [DjangoModelPermissions()]


class SingleMenuItemView(generics.RetrieveUpdateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticatedOrReadOnly()]
        else:
            return [DjangoModelPermissions()]
