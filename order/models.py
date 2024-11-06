from django.db import models
from django.db import models
from user.models import Register
from products.models import Product

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE, related_name="orders")
    products = models.ManyToManyField(Product, through="OrderItem", related_name="orders")  # Many-to-Many relationship via OrderItem
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.ForeignKey("address.Address", on_delete=models.SET_NULL, null=True, related_name="orders")
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Canceled', 'Canceled')
    ], default='Pending')

    def __str__(self):
        return f"Order {self.id} by {self.user.name} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.product.title} in Order {self.order.id}"
