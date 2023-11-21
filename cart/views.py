from django.shortcuts import redirect, get_object_or_404
from goods.models import Product
from coupons.forms import CouponApplyForm
from .cart import Cart
from .forms import CartAddProductForm
from django.views.generic import TemplateView, View


class CartAddView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product,
                    quantity=cd['quantity'],
                    override_quantity=cd['override'])
        return redirect('cart:cart_detail')


class CartRemoveView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('cart:cart_detail')


class CartView(TemplateView):
    template_name = 'cart/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(
                initial={
                    'quantity': item['quantity'],
                    'override': True}
            )
        coupon_apply_form = CouponApplyForm()
        context = {
            'cart': cart,
            'coupon_apply_form': coupon_apply_form
        }
        return context
