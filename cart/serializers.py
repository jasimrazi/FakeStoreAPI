from rest_framework import serializers
from products.models import Product, ProductImage  # For Product and ProductImage
from cart.models import Cart, CartItem  # For Cart and CartItem

# Serializer for ProductImage
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image_url']

# Serializer for Product Details (title, price, images)
class ProductDetailsSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)  # Serialize multiple images

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'images']

# Serializer for CartItem (each cart item contains a product and size)
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductDetailsSerializer()  # Serialize product details
    size = serializers.CharField()

    class Meta:
        model = CartItem
        fields = ['product', 'size']  # Include only size, no quantity

    def to_representation(self, instance):
        # Get the original representation
        representation = super().to_representation(instance)

        # Extract product data and flatten it
        product_data = representation.pop('product', {})

        # Return the flattened representation with the size
        return {**product_data, 'size': instance.size}

# Serializer for Cart (contains cart items)
class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True)  # Serialize multiple cart items

    class Meta:
        model = Cart
        fields = ['id', 'cart_items']
