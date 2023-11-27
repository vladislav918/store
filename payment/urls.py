from django.urls import path
from .views import (
    CreateCheckoutSessionView,
    SuccessView,
    CancelView,
)
from . import webhooks


app_name = 'payment'


urlpatterns = [
    path('process/', CreateCheckoutSessionView.as_view(), name='process'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('webhook/', webhooks.stripe_webhook, name='stripe-webhook'),
]
