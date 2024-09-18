from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())  # Reference product by its ID

    class Meta:
        model = CartItem
        fields = ['product', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)  # Handle multiple CartItem instances

    class Meta:
        model = Cart
        fields = ['product', 'date_created', 'items']  # Include all necessary fields

    def create(self, validated_data):
        # Extract items from the validated data
        items_data = validated_data.pop('items')
        
        # Create the cart first
        cart = Cart.objects.create(**validated_data)

        # Create the CartItem objects and associate them with the cart
        for item_data in items_data:
            CartItem.objects.create(cart=cart, **item_data)
        
        return cart

    def update(self, instance, validated_data):
        # Update the cart
        items_data = validated_data.pop('items')
        instance.product = validated_data.get('product', instance.product)
        instance.save()

        # Update or create CartItems
        for item_data in items_data:
            CartItem.objects.update_or_create(cart=instance, **item_data)

        return instance
