from rest_framework import serializers
from .models import Product, ProductImage, Size

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'
        

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)  # List of images for the product
    sizes = SizeSerializer(many=True, read_only=True)  # List of sizes for the product

    class Meta:
        model = Product
        fields = '__all__'
        
