from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import InitSubscribe, my_webhook_view
# from .webhooks import
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('webhook-subscription/', my_webhook_view, name='webhook'),
    path('subscribe/', InitSubscribe.as_view(), name='example'),
]


# router = DefaultRouter()
# router.register(r'transactions', TransactionViewSet,
# basename='transactions')
# router.register(r'expense', views.ExpenseViewSet, basename='expense')
# urlpatterns = router.urls
