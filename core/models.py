from django.db import models
from account.models import CustomUser

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    stripe_product_id = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Price(models.Model):

    stripe_price_id = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.CharField(max_length=20)
    currency = models.CharField(max_length=10)
    recurring = models.CharField(max_length=50)
    interval_count = models.IntegerField()

    def __str__(self):
        return self.product.name
