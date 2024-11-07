from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)  # For user identification
    username = serializers.CharField(source='user.name', read_only=True)  # Include username
    product_id = serializers.IntegerField(source='product.id', read_only=True)  # For product identification

    class Meta:
        model = Review
        fields = ['user_id','username', 'product_id', 'rating', 'comment', 'date_created', 'date_updated']
