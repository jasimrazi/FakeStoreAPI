from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.shortcuts import get_object_or_404
from .models import Review
from .serializers import ReviewSerializer
from products.models import Product
from user.models import Register

class AddReviewView(GenericAPIView):
    serializer_class = ReviewSerializer

    def post(self, request, product_id, loginid):
        # Extract rating and comment from the request data
        rating = request.data.get('rating')
        comment = request.data.get('comment')

        # Validate required fields
        if rating is None or comment is None:
            return Response({"error": "Rating and comment are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the product based on product_id
        product = get_object_or_404(Product, id=product_id)

        # Retrieve the user based on loginid (UUID handling)
        try:
            user = Register.objects.get(loginid__loginid=loginid)  # Directly fetch user by `loginid`
        except Register.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if a review by this user for this product already exists
        review, created = Review.objects.update_or_create(
            user=user, product=product,
            defaults={'rating': rating, 'comment': comment}
        )

        if created:
            return Response({"message": "Review added successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Review updated successfully"}, status=status.HTTP_200_OK)
