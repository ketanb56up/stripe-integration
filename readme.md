# Stripe Integration
## Steps to follow
- Need To add API keys in environment variable
- Database is alerady there with following admin credentials
username = amdin
password = pass
- Also there is test user with following credentials
username = test
password = p@ssword123
- First have to run django server
- then run  in new shell "stripe listen --forward-to localhost:8000/api/webhook-subscription/" for listening to stripe events.
- Whenever new product and price is added on stripe dashboard then product and prioce is also created in django's local database
- For subscribing to new product need to hit API "/api/create_customer/" with post request (need logged in user).
 Post request body need to have product_id and price_id of local django's instance
- User credentials can be send as Basic Auth with credentials in Postman.
- When above API hits, following  instances are created.
  Customer (if not present in database)
    PaymentMethod
    Subscription
- Hooks are listinging for product , price and subscription (update and create) 
- Demo Card details are hardcoed for deno purpose


Dependencies
python requirements are in requirement.txt.
Need to install stripe-cli for listinging to stripe events

Admin url
http://127.0.0.1:8000/api/create_customer/

Subscription Url 
http://127.0.0.1:8000/api/create_customer/

webhook url
localhost:8000/api/webhook-subscription/