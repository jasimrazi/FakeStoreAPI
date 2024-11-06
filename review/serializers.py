from rest_framework import serializers
from .models import Review
from products.serializers import ProductSerializer  # If needed to display product details

class ReviewSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Optional: serialize product details if necessary
    user_id = serializers.IntegerField(source='user.id', read_only=True)  # For user identification
    product_id = serializers.IntegerField(source='product.id', read_only=True)  # For product identification

    class Meta:
        model = Review
        fields = ['user_id', 'product_id', 'rating', 'comment', 'date_created', 'date_updated']
