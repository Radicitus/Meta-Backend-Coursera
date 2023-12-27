from LittleLemonAPI.models import Cart
from LittleLemonAPI.permissions import IsCustomer
from LittleLemonAPI.serializers import CartSerializer
from rest_framework import generics


class CartView(generics.ListCreateAPIView, generics.DestroyAPIView):
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get_permissions(self):
        return [IsCustomer()]
