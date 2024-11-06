from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import AddressSerializer
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
        mutable_data['user'] = user.id  # Add the user to the address data

        # Create the address instance using the modified data
        serializer = self.get_serializer(data=mutable_data)
        
        if serializer.is_valid():
            serializer.save()  # Save the address instance
            return Response({"message": "Address added successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
