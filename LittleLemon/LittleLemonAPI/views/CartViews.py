from rest_framework.response import Response
from LittleLemonAPI.models import Cart
from LittleLemonAPI.permissions import IsCustomer
from LittleLemonAPI.serializers import CartSerializer
from rest_framework import generics, status


class CartView(generics.ListCreateAPIView):
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def delete(self, request):
        cart = Cart.objects.filter(user=self.request.user)
        cart.delete()
        return Response("Cart successfully deleted.", status.HTTP_200_OK)

    def get_permissions(self):
        return [IsCustomer()]
