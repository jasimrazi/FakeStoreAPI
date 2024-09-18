from django.db import models

# Create your models here.
class Login(models.Model):
        email = models.EmailField(max_length=50)
        password = models.CharField(max_length=50)
        role = models.CharField(max_length=10)

    
    
class Register(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    number = models.CharField(max_length=10)
    role = models.CharField(max_length=10)
    password = models.CharField(max_length=50)
    loginid = models.OneToOneField(Login,on_delete=models.CASCADE)
