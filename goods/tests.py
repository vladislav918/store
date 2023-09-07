from mixer.backend.django import mixer
from django.test import TestCase
from django.urls import reverse
from goods.models import Category, Product
from cart.forms import CartAddProductForm


class TestProductListViews(TestCase):
    def setUp(self):
        self.category = mixer.blend(Category)
        self.product1 = mixer.blend(Product, category=self.category)
        self.product2 = mixer.blend(Product, category=self.category, available=False)
        self.url = reverse('goods:product_list')
        self.url_with_category = reverse(
            'goods:product_list_by_category',
            kwargs={'category_slug': self.category.slug},
        )

    def test_product_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'goods/list.html')
        self.assertContains(response, self.product1.name)
        self.assertNotContains(response, self.product2.name)

    def test_product_list_view_with_category(self):
        response = self.client.get(self.url_with_category)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'goods/list.html')
        self.assertContains(response, self.product1.name)
        self.assertNotContains(response, self.product2.name)

    def test_product_list_view_with_invalid_category(self):
        invalid_url = reverse(
            'goods:product_list_by_category',
            kwargs={'category_slug': 'invalid-slug'},
        )
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, 404)


class SearchResultsListViewTestCase(TestCase):
    def setUp(self):
        self.product1 = mixer.blend(Product, name='Test Product')

    def test_valid_search_query(self):
        response = self.client.get(reverse('goods:search_results'), {'q': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'goods/search_results.html')
        self.assertQuerysetEqual(
            response.context['goods'].values_list('name', flat=True),
            ['Test Product'],
        )

    def test_invalid_search_query(self):
        response = self.client.get(reverse('goods:search_results'), {'q': 'Invalid'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'goods/search_results.html')
        self.assertQuerysetEqual(response.context['goods'], [])

    def test_empty_search_query(self):
        response = self.client.get(reverse('goods:search_results'), {'q': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'goods/search_results.html')
        self.assertQuerysetEqual(
            response.context['goods'].values_list('name', flat=True),
            ['Test Product'],
        )

    def test_special_character_search_query(self):
        response = self.client.get(reverse('goods:search_results'), {'q': '!@#$%^&*()'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'goods/search_results.html')
        self.assertQuerysetEqual(response.context['goods'], [])

    def test_number_search_query(self):
        response = self.client.get(reverse('goods:search_results'), {'q': '123'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'goods/search_results.html')
        self.assertQuerysetEqual(response.context['goods'], [])

    def test_case_insensitive_search_query(self):
        response = self.client.get(reverse('goods:search_results'), {'q': 'TeSt'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'goods/search_results.html')
        self.assertQuerysetEqual(
            response.context['goods'].values_list('name', flat=True),
            ['Test Product'],
        )

    def test_multiple_word_search_query(self):
        response = self.client.get(reverse('goods:search_results'), {'q': 'test product'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'goods/search_results.html')
        self.assertQuerysetEqual(
            response.context['goods'].values_list('name', flat=True),
            ['Test Product'],
        )


class ProductDetailViewTestCase(TestCase):
    def setUp(self):
        category = Category.objects.create(name='Test Category', slug='test-category')
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            category=category,
            price=10,
            available=True,
        )

    def test_product_detail_view(self):
        response = self.client.get(
            reverse('goods:product_detail',
                    args=[self.product.id, self.product.slug],)
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'goods/detail.html')
        self.assertContains(response, self.product.name)
        self.assertContains(response, self.product.price)
        self.assertIsInstance(response.context['cart_product_form'], CartAddProductForm)

    def test_product_detail_view_with_invalid_id(self):
        url = reverse('goods:product_detail', args=[1000, 'invalid-slug'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_product_detail_view_with_unavailable_product(self):
        self.product.available = False
        self.product.save()
        response = self.client.get(
            reverse('goods:product_detail',
                    args=[self.product.id, self.product.slug],)
        )
        self.assertEqual(response.status_code, 404)
