from rest_framework import serializers
from .models import Favourite
from products.serializers import ProductSerializer  # Assuming you have a ProductSerializer

class FavouriteSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Ensures full product data is serialized
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    date_added = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Favourite
        fields = ['user_id', 'product', 'date_added']

    def to_representation(self, instance):
        # Get the original representation
        representation = super().to_representation(instance)
        
        # Extract the product data (which is now a dictionary with full product details)
        product_data = representation.pop('product', {})

        # Merge product data at the top level
        return {**representation, **product_data}
