from django.urls import path
from .views import exchange_rate_view

app_name = 'converter'

urlpatterns = [
    path('exchange-rate/', exchange_rate_view, name='exchange_rate'),
]
