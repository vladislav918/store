import stripe
from django.conf import settings
from orders.models import Order
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import TemplateView
from decimal import Decimal
from django.views import View


stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(View):
    def get(self, request):
        order_id = request.session.get('order_id', None)
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'payment/procces.html', locals())

    def post(self, request):
        order_id = request.session.get('order_id', None)
        order = get_object_or_404(Order, id=order_id)
        domain = "http://0.0.0.0:8000"
        line_items = []
        for item in order.items.all():
            line_items.append({
                'price_data': {
                    'unit_amount': int(item.price * Decimal('100')),
                    'currency': 'usd',
                    'product_data': {
                        'name': item.product.name,
                    },
                },
                'quantity': item.quantity,
            })
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            metadata={'order_id': order_id},
            success_url=domain + '/payment/success/',
            cancel_url=domain + '/payment/cancel/',
        )
        return redirect(checkout_session.url, code=303)


class SuccessView(TemplateView):
    template_name = 'payment/success.html'


class CancelView(TemplateView):
    template_name = 'payment/cancel.html'
