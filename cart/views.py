from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from products.models import Product
from .models import Cart, CartItem
from user.models import Register, Login
from . serializers import CartSerializer


class AddToCartView(GenericAPIView):
    def post(self, request, loginid):
        # Get product ID and quantity from the request
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)  # Default to 1 if not provided

        # Ensure product ID is provided
        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the product, or return a 404 error if not found
        product = get_object_or_404(Product, id=product_id)

        # Retrieve the user from Register, or return a 404 error if user does not exist
        user = get_object_or_404(Register, loginid=loginid)

        # Create or get the cart for the user (don't create a new cart for each product)
        cart, created = Cart.objects.get_or_create(user=user)

        # Check if the product is already in the cart
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not item_created:
            # If the cart item already exists, update its quantity
            cart_item.quantity += quantity
            cart_item.save()
        else:
            # Set the quantity for the new cart item
            cart_item.quantity = quantity
            cart_item.save()

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
    def get(self, request, loginid):
        # Retrieve the user based on loginid
        try:
            user = Register.objects.get(loginid=loginid)  # This correctly gets the user by loginid
        except Register.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Now use the user instance to filter carts
        carts = Cart.objects.filter(user=user)

        if carts.exists():
            serializer = CartSerializer(carts, many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No cart items found for this user"}, status=status.HTTP_400_BAD_REQUEST)

        
class UpdateCartView(GenericAPIView):
    def put(self, request, loginid):
        # Retrieve the cart for the user
        cart = get_object_or_404(Cart, loginid=loginid)

        # Get items data from the request
        items_data = request.data.get('items', [])

        # Check if items_data is empty or not a list
        if not isinstance(items_data, list):
            return Response({"error": "Invalid data format. 'items' should be a list."}, status=status.HTTP_400_BAD_REQUEST)

        if not items_data:
            return Response({"message": "No items provided to update the cart."}, status=status.HTTP_400_BAD_REQUEST)

        # Clear existing cart items
        cart.items.clear()

        # Process each item in the request
        for item_data in items_data:
            product_id = item_data.get('product_id')
            quantity = item_data.get('quantity')

            if not product_id or not quantity:
                return Response({"error": "Both 'product_id' and 'quantity' are required for each item."}, status=status.HTTP_400_BAD_REQUEST)

            # Get or create CartItem
            product = get_object_or_404(Product, id=product_id)
            cart_item, created = CartItem.objects.get_or_create(product=product, defaults={'quantity': quantity})

            if not created:
                # Update quantity if item already exists
                cart_item.quantity = quantity
                cart_item.save()

            # Add item to the cart
            cart.items.add(cart_item)

        return Response({"message": "Cart updated successfully"}, status=status.HTTP_200_OK)
    
        
class DeleteCartView(GenericAPIView):
    def delete(self, request, loginid):
        # Check if the user exists
        if not Register.objects.filter(id=loginid).exists():
            return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve the cart for the user
        cart = Cart.objects.filter(user_id=loginid).first()
        
        if not cart:
            return Response({"message": "Cart does not exist for this user"}, status=status.HTTP_404_NOT_FOUND)

        # Clear all items from the cart
        cart.items.clear()

        # Delete the cart
        cart.delete()

        return Response({"message": "Cart deleted successfully"}, status=status.HTTP_200_OK)
