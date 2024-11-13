from django.db import models
from products.models import Product  
from user.models import Register

class Cart(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE, related_name='carts')  # Related name for easier access
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.name} (created on {self.date_created})"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')  # Cart field to associate each item with a specific cart
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.quantity} of {self.product.title} in cart for {self.cart.user.name}"
