from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.db.models import Q
from django.views.generic import ListView



class SearchResultsListView(ListView):
    model = Product
    context_object_name = 'goods'
    template_name = 'goods/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get("q")
        return Product.objects.filter(Q(name__icontains=query))
    

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'goods/list.html',{'category': category, 'categories': categories, 'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'goods/detail.html', {'product': product, 'cart_product_form': cart_product_form})