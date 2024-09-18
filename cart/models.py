from django.db import models
from products.models import Product  
from user.models import Register

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE, default=1)  
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField('CartItem', related_name='cart_items')
    
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    
