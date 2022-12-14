from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

roles = (
    ("Buyer", "Buyer"),
    ("Seller", "Seller")
)


class User(AbstractUser):
    deposit = models.FloatField(null=True, default=0.0)
    role = models.CharField(null=False, choices=roles, max_length=50)


class Product(models.Model):
    amountAvailable = models.IntegerField(null=True)  # multiples of five
    cost = models.FloatField(null=True)  # multiples of five
    productName = models.CharField(max_length=100, null=True)
    sellerId = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(default=timezone.now)
