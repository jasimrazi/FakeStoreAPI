from rest_framework import serializers
from .models import Favourite
from products.models import Product

class FavouriteItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Favourite
        fields = ['product']  # Assuming you only want to capture the product ID

class FavouriteSerializer(serializers.ModelSerializer):
    items = FavouriteItemSerializer(many=True)  # List of favorite items
    user_id = serializers.IntegerField(source='user.id', read_only=True)  # Include the user_id

    class Meta:
        model = Favourite
        fields = ['user_id', 'date_added', 'items']  # Change to date_added for correct field name

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        favourite = Favourite.objects.create(**validated_data)  # Create the Favourite instance

        for item_data in items_data:
            Favourite.objects.create(user=favourite.user, product=item_data['product'])

        return favourite

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)  # Get items data if provided

        # Update the Favourite instance
        instance.save()

        # Clear existing items
        if items_data:
            instance.product.clear()  # Clear existing items before adding new ones

            for item_data in items_data:
                product = item_data.get('product')
                # Create or update the FavouriteItem
                Favourite.objects.update_or_create(
                    user=instance.user, product=product
                )

        return instance
