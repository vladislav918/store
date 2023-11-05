from django.shortcuts import redirect, get_object_or_404
from django.db.models import Q
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.generic import DetailView, CreateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


class SearchResultsListView(ListView):
    model = Product
    context_object_name = 'goods'
    template_name = 'goods/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Product.objects.filter(Q(name__icontains=query))


class ProductListView(ListView):
    model = Product
    template_name = 'goods/list.html'
    context_object_name = 'products'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = self.get_queryset().filter(category=category)
            paginator = Paginator(products, self.paginate_by)
            page_number = self.request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context['category'] = category
            context['categories'] = categories
            context['page_obj'] = page_obj
        return context

    def get_queryset(self):
        return self.model.objects.filter(available=True)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'goods/detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'id'

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        if product.favourites.filter(id=request.user.id).exists():
            product.favourites.remove(request.user)
            messages.warning(request, 'Favourites removed.')
        else:
            product.favourites.add(request.user)
            messages.success(request, 'Favourites updated.')
        return redirect('goods:product_detail', id=product.id, slug=product.slug)

    def get_object(self, queryset=None):
        product = get_object_or_404(
            Product,
            id=self.kwargs.get('id'),
            slug=self.kwargs.get('slug'),
            available=True
        )
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm()
        context['is_favourite'] = False
        if self.object.favourites.filter(id=self.request.user.id).exists():
            context['is_favourite'] = True
        return context


class FavouritesListView(LoginRequiredMixin, ListView):
    template_name = 'goods/favourites.html'
    context_object_name = 'products'

    def get_queryset(self):
        categories = Category.objects.filter(
            products__favourites=self.request.user.id).distinct()
        products = []
        for category in categories:
            products.append(Product.objects.filter(category=category))
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Product
    fields = ['category', 'name', 'description', 'image', 'price']
    success_message = 'Item successfully added!'
    template_name = 'goods/create_goods.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        if 'image' in self.request.FILES:
            instance.image = self.request.FILES['image']
        instance.save()
        return super(ProductCreateView, self).form_valid(form)


class ProductUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Product
    fields = ['category', 'name', 'description', 'image', 'price']
    success_message = 'Item successfully update!'
    template_name = 'goods/update_goods.html'
    permission_required = 'goods.change_product'
