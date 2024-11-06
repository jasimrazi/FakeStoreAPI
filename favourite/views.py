from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import FavouriteSerializer
from products.models import Product
from .models import Favourite
from user.models import Register


# View to add a product to favourites
class AddToFavouritesView(GenericAPIView):
    def post(self, request, loginid):
        # Get product ID from the request
        product_id = request.data.get('product_id')

        # Ensure product ID is provided
        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the product, or return a 404 error if not found
        product = get_object_or_404(Product, id=product_id)

        # Retrieve the user based on loginid, or return a 404 error if user does not exist
        user = get_object_or_404(Register, loginid__loginid=loginid)

        # Check if the favourite exists
        favourite, created = Favourite.objects.get_or_create(user=user, product=product)

        if not created:
            # If the product is already in favourites, remove it (toggle off)
            favourite.delete()
            return Response({"message": "Product removed from favourites"}, status=status.HTTP_200_OK)
        else:
            # Product was added to favourites (toggle on)
            return Response({"message": "Product added to favourites"}, status=status.HTTP_201_CREATED)



# View to get all favourite items of a user
class GetFavouritesByLoginIDView(GenericAPIView):
    def get(self, request, loginid):
        # Retrieve the user based on loginid
        user = get_object_or_404(Register, loginid__loginid=loginid)

        # Retrieve the favourites for the given user
        favourites = Favourite.objects.filter(user=user)

        if favourites.exists():
            # Serialize the favourites
            serializer = FavouriteSerializer(favourites, many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No favourite items found for this user"}, status=status.HTTP_400_BAD_REQUEST)


# View to delete a product from a user's favourites
class DeleteFavouriteView(GenericAPIView):
    def delete(self, request, loginid, product_id):
        # Retrieve the user based on loginid
        user = get_object_or_404(Register, loginid__loginid=loginid)

        # Retrieve the favourite product for the user
        favourite = Favourite.objects.filter(user=user, product_id=product_id).first()

        if favourite:
            favourite.delete()
            return Response({"message": "Favourite item deleted successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Favourite item not found"}, status=status.HTTP_404_NOT_FOUND)
