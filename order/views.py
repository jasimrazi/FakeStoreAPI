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
from products.models import Product
from user.models import Register
from .serializers import OrderSerializer
from django.shortcuts import get_object_or_404

class OrderCreateView(GenericAPIView):
    serializer_class = OrderSerializer

    def post(self, request, loginid):
        # Get the user by loginid
        user = get_object_or_404(Register, loginid__loginid=loginid)
        print(user.loginid)
        order_data = request.data

        # Calculate the total amount if not provided
        total_amount = order_data.get("total_amount")
        if total_amount is None:
            total_amount = sum(
                item["quantity"] * item["price"] for item in order_data.get("order_items", [])
            )

        # Create the order instance with the calculated total_amount
        order = Order.objects.create(
            user=user,
            shipping_address=order_data.get("shipping_address"),
            total_amount=total_amount,
            status=order_data.get("status", "Pending"),
        )

        # Loop through each order item and create it
        for item in order_data.get("order_items", []):
            product = get_object_or_404(Product, id=item["product_id"])
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item["quantity"],
                price=item["price"],
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

