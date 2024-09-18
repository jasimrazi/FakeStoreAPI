from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from user.models import Register  # Import the Register model for user
from products.models import Product  # Import the Product model


class AddToCartView(GenericAPIView):
    serializer_class = CartSerializer

    def post(self, request, userid):
        try:
            # Check if the user exists based on the passed userid
            user = Register.objects.get(id=userid)
        except Register.DoesNotExist:
            return Response({"Message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get the product_id and quantity from the request data
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)  # Default quantity to 1 if not provided

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"Message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        # Create or get the CartItem
        cart_item, created = CartItem.objects.get_or_create(product=product, quantity=quantity)

        # Create or get the Cart for the user
        cart, created = Cart.objects.get_or_create(product=product, defaults={'items': cart_item})
        cart.items.add(cart_item)

        return Response(
            {"Message": "Item added to cart successfully"},
            status=status.HTTP_200_OK,
        )
