from django.contrib import admin
from .models import StripeCustomer, StripePaymentMethod, StripeSubscription

# Register your models here.


@admin.register(StripeCustomer)
class StripeCustomerAdmin(admin.ModelAdmin):
    pass


@admin.register(StripePaymentMethod)
class StripePaymentMethodAdmin(admin.ModelAdmin):
    pass


@admin.register(StripeSubscription)
class StripeSubscriptionAdmin(admin.ModelAdmin):
    pass
