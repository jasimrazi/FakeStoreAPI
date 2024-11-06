from django.db import models
from products.models import Product
from user.models import Register

class Review(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE, related_name='reviews')  # User who posted the review
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')  # Product being reviewed
    rating = models.PositiveIntegerField()  # Rating value, e.g., 1 to 5
    comment = models.TextField(blank=True, null=True)  # Optional text for the review
    date_created = models.DateTimeField(auto_now_add=True)  # Timestamp when the review was created
    date_updated = models.DateTimeField(auto_now=True)  # Timestamp when the review was last updated

    class Meta:
        unique_together = ('user', 'product')  # A user can review a product only once
        ordering = ['-date_created']  # Show the most recent reviews first

    def __str__(self):
        return f"Review by {self.user.name} on {self.product.title} - {self.rating} Stars"
