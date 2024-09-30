from django.db import models
import uuid

# Create your models here.
class Login(models.Model):
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    role = models.CharField(max_length=10)
    loginid = models.CharField(max_length=100, unique=True, default=uuid.uuid4, editable=False)

    def save(self, *args, **kwargs):
        if not self.loginid:
            self.loginid = str(uuid.uuid4())  # Generate a unique login ID if it doesn't exist
        super().save(*args, **kwargs)


class Register(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    number = models.CharField(max_length=10)
    role = models.CharField(max_length=10, default="user")
    password = models.CharField(max_length=50)
    loginid = models.OneToOneField(Login, on_delete=models.CASCADE, related_name='register')

    def save(self, *args, **kwargs):
        if not self.loginid:
            login_instance = Login.objects.create(email=self.email, password=self.password, role=self.role)
            self.loginid = login_instance  # Link the generated Login instance
        super().save(*args, **kwargs)


class MerchantRegister(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    number = models.CharField(max_length=10)
    role = models.CharField(max_length=10, default="merchant")
    password = models.CharField(max_length=50)
    store_name = models.CharField(max_length=100)
    business_license = models.CharField(max_length=100)
    loginid = models.OneToOneField(Login, on_delete=models.CASCADE, related_name='merchant_register')

    def save(self, *args, **kwargs):
        if not self.loginid:
            login_instance = Login.objects.create(email=self.email, password=self.password, role=self.role)
            self.loginid = login_instance  # Link the generated Login instance
        super().save(*args, **kwargs)
