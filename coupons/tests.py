from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Coupon
from goods.models import Category, Product
from django.contrib.sessions.middleware import SessionMiddleware
from cart.cart import Cart
from django.test import RequestFactory
from django.contrib.auth import get_user_model


class CouponApplyTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.factory = RequestFactory()
        request = self.factory.get('/')
        request.user = self.user
        middleware = SessionMiddleware(lambda x: None)
        middleware.process_request(request)
        request.session.save()
        self.cart = Cart(request)
        category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(name='Test Product', price=10, category=category)
        self.cart.add(product=self.product)
        self.coupon = Coupon.objects.create(
            code='TESTCOUPON',
            valid_from=timezone.now(),
            valid_to=timezone.now() + timezone.timedelta(days=7),
            discount=5,
            active=True,
        )

    def test_valid_coupon(self):
        url = reverse('coupons:apply')
        data = {'code': 'TESTCOUPON'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('cart:cart_detail'))
        self.assertEqual(self.client.session['coupon_id'], self.coupon.id)

    def test_invalid_coupon(self):
        url = reverse('coupons:apply')
        data = {'code': 'INVALIDCOUPON'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('cart:cart_detail'))
        self.assertIsNone(self.client.session.get('coupon_id'))
