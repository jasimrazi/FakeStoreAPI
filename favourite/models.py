from django.db import models
from products.models import Product  
from user.models import Register

# Create your models here.

class Favourite(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)  # The user who has marked products as favorites
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # The product marked as a favorite
    date_added = models.DateTimeField(auto_now_add=True)  # Timestamp for when the product was added to favorites

    class Meta:
        unique_together = ('user', 'product')  # Ensure a user can favorite a product only once

    def __str__(self):
        return f"{self.user.name} - {self.product.title}"
