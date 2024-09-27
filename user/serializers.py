from rest_framework import serializers
from . models import Register, Login, MerchantRegister

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = '__all__'
        
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = '__all__'


class MerchantRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantRegister
        fields = '__all__'

