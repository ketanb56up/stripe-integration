import stripe
from django.conf import settings
STRIPE_SETTING = getattr(settings, 'STRIPE_SETTING', {})
stripe.api_key = STRIPE_SETTING["STRIPE_SECRET_KEY"]

stripe.PaymentMethod.create(
    type="card",
    card={
        "number": "4242424242424242",
        "exp_month": 8,
        "exp_year": 2022,
        "cvc": "314",
    },
)


def initPayment(request, id):
        checkout_session = stripe.checkout.Session.create(
        # Customer Email is optional,
        # It is not safe to accept email directly from the client side
        customer_email=request_data['email'],
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                    'name': product.name,
                    },
                    'unit_amount': int(product.price * 100),
                },
                'quantity': 1,
            }
        ],
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('success')
        ) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('failed')),
    stripe.PaymentMethod.create(
        type="card",
        card={
            "number": "4242424242424242",
            "exp_month": 8,
            "exp_year": 2022,
            "cvc": "314",
        },
    )

    def createPaymentMethod(self):
        stripe.api_key=STRIPE["key"]
        stripe.PaymentMethod.create(
        type="card",
        card={
            "number": "4242424242424242",
            "exp_month": 8,
            "exp_year": 2022,
            "cvc": "314",
        },
        )
