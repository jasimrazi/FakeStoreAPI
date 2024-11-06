from rest_framework import serializers
from .models import Favourite
from products.serializers import ProductSerializer  # Assuming you have a ProductSerializer

class FavouriteSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Serialize product details if needed
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = Favourite
        fields = ['user_id', 'product', 'date_added']
