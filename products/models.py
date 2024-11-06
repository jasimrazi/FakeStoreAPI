from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)  # Increased length for more details
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Use DecimalField for currency
    category = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    sizes = models.ManyToManyField('Size', related_name="products")  # Many-to-many relationship with Size

    def __str__(self):
        return self.title

class Size(models.Model):
    size = models.CharField(max_length=10, unique=True)  # Ensure sizes are unique, like "S", "M", "L"

    def __str__(self):
        return self.size

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image_url = models.URLField(max_length=200)

    def __str__(self):
        return f"Image for {self.product.title}"
