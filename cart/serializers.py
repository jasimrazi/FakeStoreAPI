from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product
from user.models import Login  # Assuming Login is the model with loginid

class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    user_loginid = serializers.CharField(source='user.loginid', read_only=True)  # Use loginid instead of user_id
    items = CartItemSerializer(many=True)  # Include items for serialization

    class Meta:
        model = Cart
        fields = ['user_loginid', 'date_created', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        cart = Cart.objects.create(**validated_data)

        for item_data in items_data:
            CartItem.objects.create(cart=cart, **item_data)

        return cart

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', [])
        instance.save()  # Save instance to update other fields if necessary

        # Clear existing items before adding new ones
        instance.items.clear()

        for item_data in items_data:
            CartItem.objects.create(cart=instance, **item_data)

        return instance
