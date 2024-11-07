from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import AddressSerializer
from .models import Address  # Import Address model
from user.models import Register

class AddAddressView(GenericAPIView):
    serializer_class = AddressSerializer

    def post(self, request, loginid):
        try:
            # Retrieve the user based on loginid
            user = Register.objects.get(loginid__loginid=loginid)
        except Register.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Create a mutable copy of the request data and add the user to it
        mutable_data = request.data.copy()
        mutable_data['user'] = user.id

        # Check if this address is being added as the default
        is_default = mutable_data.get('is_default', False)

        if is_default:
            # If a default address already exists for this user, set it to non-default
            Address.objects.filter(user=user, is_default=True).update(is_default=False)

        # Create the address instance using the modified data
        serializer = self.get_serializer(data=mutable_data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Address added successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class GetAddressView(GenericAPIView):
    serializer_class = AddressSerializer

    def get(self, request, loginid):
        # Retrieve the user based on loginid
        try:
            user = Register.objects.get(loginid__loginid=loginid)
        except Register.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Fetch all addresses for the user
        addresses = Address.objects.filter(user=user)
        
        if not addresses.exists():
            return Response({"message": "No addresses found for this user"}, status=status.HTTP_404_NOT_FOUND)

        # Serialize and return the addresses
        serializer = self.get_serializer(addresses, many=True)
        return Response({"addresses": serializer.data}, status=status.HTTP_200_OK)
