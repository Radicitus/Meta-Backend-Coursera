from django_filters.rest_framework import DjangoFilterBackend
from LittleLemonAPI.models import MenuItem
from LittleLemonAPI.serializers import MenuItemSerializer
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, DjangoModelPermissions


class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['category', 'featured']
    ordering_fields = ['price', 'title']

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
