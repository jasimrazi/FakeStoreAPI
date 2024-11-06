# serializers.py
from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer  # If you need to display product details

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    loginid = serializers.CharField(source='user.loginid.loginid', read_only=True)  # Use loginid instead of user id
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'loginid', 'shipping_address', 'total_amount', 'status', 'order_date', 'order_items']
