from django.db import models
from user.models import Register  # Assuming the user model is in the 'user' app

class Address(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE, related_name="addresses")
    name = models.CharField(max_length=255)  # Name of the recipient
    address = models.CharField(max_length=255)  # Full street address
    city = models.CharField(max_length=100)  # City
    country = models.CharField(max_length=100)  # Country
    phone_number = models.CharField(max_length=20)  # Phone number
    is_default = models.BooleanField(default=False)  # Default address flag
    date_added = models.DateTimeField(auto_now_add=True)  # Timestamp when the address is added

    def __str__(self):
        return f"{self.name} - {self.city}, {self.country}"

    class Meta:
        # Ensure a user can have only one default address
        unique_together = ('user', 'is_default')
