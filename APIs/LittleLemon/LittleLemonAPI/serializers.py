from decimal import Decimal
from sqlite3 import Date

from rest_framework import serializers, status
from rest_framework.response import Response

from .models import MenuItem, Category, Cart, Order, OrderItem
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category']


class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    menu_item = MenuItemSerializer()
    total = serializers.SerializerMethodField()

    @staticmethod
    def get_total(cart: Cart):
        return cart.quantity * cart.menu_item.price

    def create(self, validated_data):
        user = self.context['request'].user
        menu_item = MenuItem.objects.get(**validated_data.pop('menu_item'))
        quantity = validated_data.pop('quantity')

        new_cart = Cart.objects.create(user=user, menu_item=menu_item, quantity=quantity)
        return new_cart

    class Meta:
        model = Cart
        fields = ['id', 'user', 'menu_item', 'quantity', 'total']


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    delivery_crew = UserSerializer(read_only=True)
    status = serializers.BooleanField(read_only=True)
    total = serializers.DecimalField(read_only=True, max_digits=6, decimal_places=2)
    date = serializers.DateField(read_only=True)

    def create(self, validated_data):
        user = self.context['request'].user

        # Get cart of user
        cart = Cart.objects.filter(user=user)

        # Return empty list if cart is empty
        if cart.count() < 1:
            return []

        # Get total price for all items in cart
        total = Decimal()
        for cart_item in cart:
            total += cart_item.menu_item.price * cart_item.quantity

        # Create order object
        new_order = Order.objects.create(user=user, total=total, date=Date.today())

        # Convert cart items into order items
        for cart_item in cart:
            OrderItem.objects.create(order=new_order, menu_item=cart_item.menu_item,
                                     quantity=cart_item.quantity)

        # Empty cart
        cart.delete()

        return new_order

    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date']


class OrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    menu_item = MenuItemSerializer(read_only=True)
    quantity = serializers.DecimalField(read_only=True, max_digits=6, decimal_places=2)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'menu_item', 'quantity']
