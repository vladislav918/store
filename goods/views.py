from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.views.generic import ListView
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.decorators.cache import cache_page


class SearchResultsListView(ListView):
    model = Product
    context_object_name = 'goods'
    template_name = 'goods/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Product.objects.filter(Q(name__icontains=query))


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    paginator = Paginator(products, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    context = {
        'category': category,
        'categories': categories,
        'page_obj': page_obj,
    }
    return render(request, 'goods/list.html', context=context)


@login_required
def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    if request.method == 'POST':
        if product.favourites.filter(id=request.user.id).exists():
            product.favourites.remove(request.user)
            messages.warning(request, 'Favourites removed.')
        else:
            product.favourites.add(request.user)
            messages.success(request, 'Favourites updated.')
        return redirect('goods:product_detail', id=id, slug=slug)

    is_favourite = False
    if product.favourites.filter(id=request.user.id).exists():
        is_favourite = True

    cart_product_form = CartAddProductForm()
    context = {
        'product': product,
        'cart_product_form': cart_product_form,
        'is_favourite': is_favourite,
    }
    return render(request, 'goods/detail.html', context=context)


@login_required
def favourites(request):
    categories = Category.objects.filter(products__favourites=request.user.id).distinct()
    products = []
    for category in categories:
        products.append(Product.objects.filter(category=category))

    context = {
        'products': products,
    }
    
    return render(request, 'goods/favourites.html', context=context)
