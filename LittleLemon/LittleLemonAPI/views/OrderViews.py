from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from LittleLemonAPI.models import Order, OrderItem
from LittleLemonAPI.permissions import IsCustomer, IsManager, IsDeliveryCrew
from LittleLemonAPI.serializers import OrderSerializer, OrderItemSerializer
from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticated


class OrdersView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'delivery_crew', 'date', 'user']
    ordering_fields = ['total', 'status', 'delivery_crew', 'date', 'user']

    def get_queryset(self):
        if IsManager.check(self.request):
            return Order.objects.all()
        if IsCustomer.check(self.request):
            return Order.objects.filter(user=self.request.user)
        if IsDeliveryCrew.check(self.request):
            return Order.objects.filter(delivery_crew=self.request.user)

    def get_permissions(self):
        return [IsAuthenticated()]


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def SingleOrderView(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except:
        return Response("Order does not exist.", status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        if order.user == request.user or IsManager.check(request):
            order_items = OrderItem.objects.filter(order=order)
            order_items_serializer = OrderItemSerializer(order_items, many=True)
            order_items_serializer_data = order_items_serializer.data
            return Response(order_items_serializer_data, status.HTTP_200_OK)
        else:
            return Response("You are not authorized to view this order.", status.HTTP_401_UNAUTHORIZED)

    if request.method == 'PATCH':
        if IsDeliveryCrew.check(request) or IsManager.check(request):
            order_status = request.data.get('status')
            if order_status:
                order.status = order_status
                order.save()

                return Response("Order status has been updated.", status.HTTP_200_OK)
            else:
                return Response("Missing status parameter.", status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        if IsManager.check(request):
            delivery_crew_name = request.data.get('delivery_crew')

            if delivery_crew_name:
                try:
                    delivery_crew = User.objects.get(username=delivery_crew_name)
                except User.DoesNotExist:
                    return Response("Delivery crew does not exist.", status.HTTP_400_BAD_REQUEST)

                order.delivery_crew = delivery_crew
                order.save()

                return Response(f"Order delivery crew has been updated to {delivery_crew_name}.", status.HTTP_200_OK)

            return Response("Missing delivery crew name parameter.", status.HTTP_400_BAD_REQUEST)

        else:
            return Response("You are not authorized to update this order.", status.HTTP_401_UNAUTHORIZED)

    if request.method == 'DELETE':
        if IsManager.check(request):
            order.delete()
            return Response("Order has been deleted.", status.HTTP_200_OK)
        else:
            return Response("You are not authorized to delete this order.", status.HTTP_401_UNAUTHORIZED)
