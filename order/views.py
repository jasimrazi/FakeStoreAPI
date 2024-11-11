# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.shortcuts import get_object_or_404
from .models import Order, OrderItem
from user.models import Register
from products.models import Product
from .serializers import OrderSerializer

# views.py
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem
from address.models import Address
from products.models import Product
from user.models import Register
from .serializers import OrderSerializer
from django.shortcuts import get_object_or_404

class OrderCreateView(GenericAPIView):
    serializer_class = OrderSerializer

    def post(self, request, loginid):
        # Get the user by loginid
        user = get_object_or_404(Register, loginid__loginid=loginid)
        order_data = request.data

        # Retrieve the Address instance based on the ID provided in the request
        address_id = order_data.get("shipping_address")
        shipping_address = get_object_or_404(Address, id=address_id)

        # Ensure total_amount is provided in the request data
        total_amount = order_data.get("total_amount")
        if total_amount is None:
            return Response(
                {"error": "total_amount is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create the order with the provided total amount
        order = Order.objects.create(
            user=user,
            shipping_address=shipping_address,
            total_amount=total_amount,
            status=order_data.get("status", "Pending"),
        )

        # Add each order item to the order, setting price from the product
        for item in order_data.get("order_items", []):
            product = get_object_or_404(Product, id=item["product_id"])
            price = product.price  # Get the product's price
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item["quantity"],
                price=price,  # Pass the price dynamically
            )

        # Serialize and return the created order
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)






class UserOrderListView(GenericAPIView):
    serializer_class = OrderSerializer

    def get(self, request, loginid):
        # Get the user by loginid
        user = get_object_or_404(Register, loginid__loginid=loginid)

        # Get all orders for the user
        orders = Order.objects.filter(user=user)

        # Serialize the list of orders
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

