from rest_framework import serializers
from .models import StripeCustomer, StripePaymentMethod, StripeSubscription


class StripeCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StripeCustomer
        fields = '__all__'


class StripePaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = StripePaymentMethod
        fields = '__all__'


class StripeSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StripeSubscription
        fields = '__all__'
