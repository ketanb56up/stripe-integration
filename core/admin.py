from django.contrib import admin
from .models import Product, Price

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('product', 'price')
