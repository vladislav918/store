from django.shortcuts import render, redirect
from django.urls import reverse
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin


class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        form = OrderCreateForm()
        context = {
            'cart': cart,
            'form': form,
        }
        return render(request, 'orders/create.html', context=context)

    def post(self, request):
        cart = Cart(request)
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            request.session['order_id'] = order.id
            cart.clear()

            return redirect(reverse('payment:process'))
        context = {
            'cart': cart,
            'form': form,
        }
        return render(request, 'orders/create.html', context=context)
