from django.urls import path
from coupons.views import CouponView


app_name = 'coupons'

urlpatterns = [
    path('apply/', CouponView.as_view(), name='apply'),
]
