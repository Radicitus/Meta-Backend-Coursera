from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from LittleLemonAPI.models import Order, OrderItem
from LittleLemonAPI.permissions import IsCustomer, IsManager, IsDeliveryCrew
from LittleLemonAPI.serializers import OrderSerializer, OrderItemSerializer
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


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def SingleOrderView(request, order_id=None):
    if request.method == 'GET':
        if IsCustomer.check(request) and order_id is not None:
            order = Order.objects.get(id=order_id)

            if order.user == request.user:
                order_items = OrderItem.objects.filter(order=order)
                order_items_serializer = OrderItemSerializer(order_items, many=True)
                order_items_serializer_data = order_items_serializer.data
                return Response(order_items_serializer_data, status.HTTP_200_OK)
            else:
                return Response("You are not authorized to view this order.", status.HTTP_401_UNAUTHORIZED)
