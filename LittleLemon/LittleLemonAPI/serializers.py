from decimal import Decimal

from rest_framework import serializers
from .models import MenuItem, Category, Cart, Order
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

    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date']
