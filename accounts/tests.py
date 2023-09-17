from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import CustomUser, Follow
from goods.models import Product, Category
from django.urls import reverse_lazy


class CustomUserTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='will',
            email='will@email.com',
            password='testpass123',
        )
        self.assertEqual(user.username, 'will')
        self.assertEqual(user.email, 'will@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username='superadmin',
            email='superadmin@email.com',
            password='testpass123',
        )
        self.assertEqual(admin_user.username, 'superadmin')
        self.assertEqual(admin_user.email, 'superadmin@email.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class SignupTests(TestCase):
    username = 'newuser'
    email = 'newuser@email.com'

    def setUp(self):
        url = reverse('account_signup')
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'account/signup.html')
        self.assertContains(self.response, 'Sign Up')
        self.assertNotContains(self.response, 'Hi there! I should not be on the page.')

    def test_signup_form(self):
        new_user = get_user_model().objects.create_user(
            self.username, self.email)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, self.username)
        self.assertEqual(get_user_model().objects.all()[0].email, self.email)


class ProfileViewTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        category = Category.objects.create(name='Test Category', slug='test-category')
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        self.product = Product.objects.create(
            name='Test Product',
            author=self.user,
            available=True,
            slug='test-product',
            category=category,
            price=10,
        )
        self.url = reverse('accounts:profile', args=[self.user.username])

    def test_profile_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/profile.html')
        self.assertContains(response, self.user.username)
        self.assertContains(response, self.product.name)

    def test_following(self):
        user2 = CustomUser.objects.create_user(
            username='testuser2',
            email='testuser2@example.com',
            password='testpass'
        )
        self.client.force_login(user2)
        response = self.client.get(self.url)
        self.assertEqual(response.context['following'], False)
        follow = Follow.objects.create(user=user2, author=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.context['following'], True)

    def test_products_count(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context['products_count'], 1)

    def test_followers_count(self):
        user2 = CustomUser.objects.create_user(
            username='testuser2',
            email='testuser2@example.com',
            password='testpass'
        )
        follow = Follow.objects.create(user=user2, author=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.context['followers_count'], 1)


class ProfileUpdateTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        self.client.login(username='testuser', password='testpass')

    def test_profile_update_success(self):
        url = reverse_lazy('accounts:profile_update', kwargs={'pk': self.user.pk})
        data = {
            'username': 'newusername',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse_lazy(
            'accounts:profile',
            kwargs={'username': 'newusername'})
        )
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newusername')
        self.assertEqual(self.user.first_name, 'New')
        self.assertEqual(self.user.last_name, 'User')
        self.assertEqual(self.user.email, 'newuser@example.com')

    def test_profile_update_failure(self):
        url = reverse_lazy('accounts:profile_update', kwargs={'pk': self.user.pk})
        data = {
            'username': '',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')
