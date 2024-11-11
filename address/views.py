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

        # Extract address details from the request
        name = request.data.get('name')
        address = request.data.get('address')
        city = request.data.get('city')
        country = request.data.get('country')
        phone_number = request.data.get('phone_number')

        # Check if the same address already exists for the user
        if Address.objects.filter(
            user=user,
            name=name,
            address=address,
            city=city,
            country=country,
            phone_number=phone_number
        ).exists():
            return Response({"message": "Address already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # Create a mutable copy of the request data and add the user ID
        mutable_data = request.data.copy()
        mutable_data['user'] = user.id

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
    

class RemoveAddressView(GenericAPIView):
    def delete(self, request, loginid, address_id):
        # Verify the user based on loginid
        try:
            user = Register.objects.get(loginid__loginid=loginid)
        except Register.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get the specific address for the user
        try:
            address = Address.objects.get(id=address_id, user=user)
        except Address.DoesNotExist:
            return Response({"error": "Address not found for this user"}, status=status.HTTP_404_NOT_FOUND)

        # Delete the address
        address.delete()
        return Response({"message": "Address removed successfully"}, status=status.HTTP_200_OK)
