from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import StripeSubscriptionSerializer
import datetime
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import StripeCustomer, StripePaymentMethod, StripeSubscription
from core.models import Product, Price
import stripe
from django.views.decorators.csrf import csrf_exempt
import json
import os
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
# Create your views here.


class InitSubscribe(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        data = request.data
        user = request.user
        product_id = data.get("product_id")
        price_id = data.get("price_id")
        product = Product.objects.filter(id=product_id).first()
        if product:
            price = product.price_set.filter(id=price_id).first()

            stripe_customer, created = StripeCustomer.objects.get_or_create(
                user=user)
            payment_method = stripe.PaymentMethod.create(
                type="card",
                card={
                    "number": "4242424242424242",
                    "exp_month": 8,
                    "exp_year": 2022,
                    "cvc": "314",
                },
            )

            if created:
                customer = stripe.Customer.create(
                    email=data.get(user.email),
                    payment_method=payment_method.id,
                    invoice_settings={
                        "default_payment_method": payment_method.id},
                    name=data.get('name'),
                    address={
                        'line1': '510 Townsend St',
                        'postal_code': '98140',
                        'city': 'San Francisco',
                        'state': 'CA',
                        'country': 'US',
                    },
                )

                stripe_customer.stripe_customer_id = customer.id
                stripe_customer.save()

            stripe_payment_method = StripePaymentMethod.objects.create(
                stripe_payment_method_id=payment_method.id,
                billing_details=payment_method.billing_details,
                customer=stripe_customer)

            stripe.PaymentMethod.attach(
                payment_method.id,
                customer=stripe_customer.stripe_customer_id
            )

            subscription = stripe.Subscription.create(
                customer=stripe_customer.stripe_customer_id,
                items=[
                    {"price": price.stripe_price_id},
                ],
                payment_behavior='default_incomplete',
                expand=['latest_invoice.payment_intent'],
            )

            stripe_subscription = StripeSubscription.objects.create(
                stripe_subscription_id=subscription.id,
                latest_invoice_id=subscription.latest_invoice,
                status=subscription.status,
                stripe_payment_method=stripe_payment_method, price=price,
                start_date=datetime.datetime.fromtimestamp(
                    int(subscription.current_period_start)
                ).strftime('%Y-%m-%d %H:%M:%S'))
            stripe_payment_method.save()

            subscription_serializer = StripeSubscriptionSerializer(
                stripe_subscription)

            return Response(data=subscription_serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(data={"Error": "Product Not Found"},
                        status=status.HTTP_404_NOT_FOUND)


@ api_view(['GET', 'POST'])
@ permission_classes((AllowAny, ))
@ csrf_exempt
def my_webhook_view(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        # Invalid payload
        return Response(status=400)

    # Handle the event
    if event.type == 'customer.subscription.created':
        subscription = event.data.object

    elif event.type == 'customer.subscription.updated':
        subscription = event.data.object
        stripe_subscription, created = StripeSubscription.objects.get_or_create(
            stripe_subscription_id=subscription.id
        )
        if not created:
            stripe_subscription.status = subscription.status

    elif event.type == 'product.created':
        product = event.data.object
        Product.objects.create(
            stripe_product_id=product.id, name=product.name, description=product.description)

    elif event.type == 'product.updated':
        stripe_product = event.data.object
        product, created = Product.objects.get_or_create(
            stripe_product_id=stripe_product.id,
            defaults={'name': stripe_product.name, 'description': stripe_product.description})
        if not created:
            product.name = stripe_product.name
            product.description = stripe_product.description
            product.save()

    elif event.type == 'price.created':
        stripe_price = event.data.object
        product = Product.objects.get(stripe_product_id=stripe_price.product)
        price = Price.objects.create(
            stripe_price_id=stripe_price.id,
            product=product,
            price=stripe_price.unit_amount_decimal,
            currency=stripe_price.currency,
            recurring=stripe_price.recurring.interval,
            interval_count=stripe_price.recurring.interval_count)

    elif event.type == 'price.updated':
        stripe_price = event.data.object
        product = Product.objects.filter(
            stripe_product_id=stripe_price.product).first()
        if product:
            price, created = Price.objects.get_or_create(
                stripe_price_id=stripe_price.id,
                defaults={'product': product, 'price': stripe_price.unit_amount_decimal,
                          'currency': stripe_price.currency, 'recurring': stripe_price.recurring.interval,
                          'interval_count': recurring.interval_count})

    else:
        print('Unhandled event type {}'.format(event.type))

    return Response(({"message": "Got some data!", "data": request.data}))
