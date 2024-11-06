from django.db import models
from products.models import Product  
from user.models import Register

class Cart(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE, related_name='carts')  # Added related_name for easier access
    date_created = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField('CartItem', related_name='cart_items')

    

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    
