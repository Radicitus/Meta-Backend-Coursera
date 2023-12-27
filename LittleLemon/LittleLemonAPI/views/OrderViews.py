from LittleLemonAPI.models import Order
from LittleLemonAPI.permissions import IsCustomer, IsManager, IsDeliveryCrew
from LittleLemonAPI.serializers import OrderSerializer
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated


class OrdersView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        if IsCustomer.check(self.request):
            return Order.objects.filter(user=self.request.user)
        if IsManager.check(self.request):
            return Order.objects.all()
        if IsDeliveryCrew.check(self.request):
            return Order.objects.filter(delivery_crew=self.request.user)

    def get_permissions(self):
        return [IsAuthenticated()]


class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_permissions(self):
        return [IsAuthenticated()]
