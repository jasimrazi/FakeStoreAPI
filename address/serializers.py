from rest_framework import serializers
from .models import Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['user','name', 'country', 'city', 'phone_number', 'address']

    def validate_phone_number(self, value):
        # Example validation for phone number (optional, depending on format)
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must be digits.")
        return value
