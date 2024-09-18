from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)  # Include the user_id

    class Meta:
        model = Cart
        fields = ['user_id', 'product', 'date_created', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        cart = Cart.objects.create(**validated_data)

        for item_data in items_data:
            CartItem.objects.create(cart=cart, **item_data)

        return cart

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items')
        instance.product = validated_data.get('product', instance.product)
        instance.save()

        for item_data in items_data:
            CartItem.objects.update_or_create(cart=instance, **item_data)

        return instance
