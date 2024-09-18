from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from products.models import Product
from .models import Cart, CartItem
from user.models import Register 
from . serializers import CartSerializer


class AddToCartView(GenericAPIView):
    def post(self, request, userid):
        # Get product ID and quantity from the request
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)  # Default to 1 if not provided

        # Ensure product ID is provided
        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the product, or return a 404 error if not found
        product = get_object_or_404(Product, id=product_id)

        # Retrieve the user, or return a 404 error if user does not exist
        user = get_object_or_404(Register, id=userid)

        # Create or get the cart for the user
        cart, created = Cart.objects.get_or_create(user=user, product=product)

        # Create a new CartItem or update an existing one if the product is already in the cart
        cart_item, item_created = CartItem.objects.get_or_create(product=product, defaults={'quantity': quantity})
        
        if not item_created:
            cart_item.quantity += quantity  # Update quantity if item already exists
            cart_item.save()

        # Add the item to the cart
        cart.items.add(cart_item)
        cart.save()

        return Response({"message": "Item added to cart successfully"}, status=status.HTTP_201_CREATED)
    
class GetAllCartItemsView(GenericAPIView):
    def get(self, request):
        # Retrieve query parameters for limit and sort
        limit = request.GET.get('limit', '10')  # Default limit to 10
        sort = request.GET.get('sort', 'asc')   # Default sort to ascending

        # Validate and convert limit to integer
        try:
            limit = int(limit)
        except ValueError:
            limit = 10  # Default to 10 if conversion fails

        # Determine the sort order
        if sort == 'desc':
            carts = Cart.objects.all().order_by('-date_created')
        else:
            carts = Cart.objects.all().order_by('date_created')  # Default ascending

        # Apply the limit to the queryset
        carts = carts[:limit]

        # Serialize the carts
        if carts.exists():
            serializer = CartSerializer(carts, many=True)
            return Response(
                {"data": serializer.data, "message": "Fetch successful"},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": "No cart items found"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
class GetCartItemUserID(GenericAPIView):

    def get(self, request, userid):
        # Filter carts by the given user ID
        carts = Cart.objects.filter(user_id=userid)
        
        if carts.exists():
            # Serialize the filtered carts
            serializer = CartSerializer(carts, many=True)
            return Response(
                {"data": serializer.data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "No cart items found for this user"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        
