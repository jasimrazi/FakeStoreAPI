from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from products.models import Product
from .models import Cart, CartItem
from user.models import Register, Login
from . serializers import CartSerializer


class AddToCartView(GenericAPIView):
    def post(self, request, loginid, productid, size):
        print("Received login ID from request:", loginid)
        print("Received product ID from URL:", productid)
        print("Received size from URL:", size)  # Debug: Size check

        # Retrieve the product and login instance
        product = get_object_or_404(Product, id=productid)
        login_instance = get_object_or_404(Login, loginid=loginid)
        user = login_instance.register

        # Get or create the cart
        cart, created = Cart.objects.get_or_create(user=user)

        # Check if the cart already contains the product with the same size
        cart_item = CartItem.objects.filter(cart=cart, product=product, size=size).first()

        if cart_item:
            # If the item already exists with the same size, return an existing message
            return Response({"message": "Item with the same size already added to cart"}, status=status.HTTP_200_OK)
        else:
            # If it's a new item, create it and set quantity to 1
            cart_item = CartItem.objects.create(cart=cart, product=product, size=size, quantity=1)
            print("New cart item created with default quantity and size:", cart_item.quantity, cart_item.size)
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
        print("Received login ID:", loginid)  # Debugging line

        # Retrieve the user based on loginid
        try:
            user = Register.objects.get(loginid__loginid=loginid)  # Correct way to access the loginid through related model
            print("Found user:", user)  # Debugging line
        except Register.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Now use the user instance to filter carts
        carts = Cart.objects.filter(user=user)
        print("Retrieved carts:", carts)  # Debugging line

        for cart in carts:
            print(f"Cart {cart.id} items:", cart.cart_items.all())  # Debugging line to check if cart has items

        if carts.exists():
            # Serialize the cart including its related CartItem instances
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
