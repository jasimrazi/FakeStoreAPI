from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    # Accessing the nested loginid attribute
    user_loginid = serializers.CharField(source='user.loginid.loginid', read_only=True)  
    cart_items = CartItemSerializer(many=True, read_only=True)  # Use 'cart_items' to match related_name in Cart model

    class Meta:
        model = Cart
        fields = ['user_loginid', 'date_created', 'cart_items']

    def update(self, instance, validated_data):
        # Remove existing cart items
        instance.cart_items.clear()

        # Extract and add new items to the cart
        items_data = validated_data.pop('cart_items', [])
        for item_data in items_data:
            CartItem.objects.create(cart=instance, **item_data)

        # Save any additional fields
        instance.save()
        return instance
