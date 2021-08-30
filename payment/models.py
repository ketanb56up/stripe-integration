from django.db import models
from account.models import CustomUser
from core.models import Price, Product

# Create your models here.


class StripeCustomer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=100)
    stripe_subscription = models.ForeignKey(
        "StripeSubscription", null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class StripePaymentMethod(models.Model):
    stripe_payment_method_id = models.CharField(max_length=100)
    billing_details = models.CharField(max_length=100)
    customer = models.ForeignKey(StripeCustomer, on_delete=models.CASCADE)

    def __str__(self):
        return self.stripe_payment_method_id


class StripeSubscription(models.Model):
    stripe_subscription_id = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    price = models.ForeignKey(Price, on_delete=models.CASCADE)
    latest_invoice_id = models.CharField(max_length=100)
    stripe_payment_method = models.ForeignKey(
        StripePaymentMethod, on_delete=models.CASCADE)

    def __str__(self):
        return self.stripe_subscription_id
