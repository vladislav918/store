from django.test import TestCase
from django.urls import reverse
from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from goods.models import Product, Category
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware


class OrderCreateViewTestCase(TestCase):
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

    def test_order_create_view_with_authenticated_user(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('orders:order_create'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'address': '123 Main St',
            'postal_code': '12345',
            'city': 'Anytown',
        })
        order = Order.objects.first()
        order_item = OrderItem.objects.create(order=order, product=self.product, quantity=1, price=self.product.price) 
        self.assertEqual(order.first_name, 'John')
        self.assertEqual(order.last_name, 'Doe')
        self.assertEqual(order.email, 'johndoe@example.com')
        self.assertEqual(order.address, '123 Main St')
        self.assertEqual(order.postal_code, '12345')
        self.assertEqual(order.city, 'Anytown')
        self.assertEqual(order_item.quantity, 1)
        self.assertEqual(order_item.price, 10)
        self.assertEqual(order_item.product, self.product)


    def test_order_create_view_with_unauthenticated_user(self):
        url = reverse('orders:order_create')
        response = self.client.post(url, {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@test.com',
            'address': 'Test Address',
            'postal_code': '12345',
            'city': 'Test City',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('account_login') + '?next=' + url)

    def test_order_create_view_with_invalid_form(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('orders:order_create')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')

    def test_order_create_view_with_get_request(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('orders:order_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], OrderCreateForm)
        self.assertTemplateUsed(response, 'orders/create.html')