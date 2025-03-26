from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField  # Use JSONField for structured data

class PasswordResetRequest(models.Model):
    email = models.EmailField()
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.CharField(max_length=255)  # Store the relative path to the static image

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    cart_items = models.JSONField(default=list)  # Use an empty list as the default value
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
