from django.shortcuts import render,redirect, get_object_or_404
from django.db.models import Q
from django.views.generic import ListView
from .models import Category, Product
from cart.forms import CartAddProductForm


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
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    context = {
        'category': category,
        'categories': categories,
        'products': products,
    }
    return render(request, 'goods/list.html', context=context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    if request.method == 'POST':
        if product.favourites.filter(id=request.user.id).exists():
            product.favourites.remove(request.user)
        else:
            product.favourites.add(request.user)
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
