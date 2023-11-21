import stripe
from django.conf import settings
from django.views import View
from orders.models import Order 
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import TemplateView
from decimal import Decimal


stripe.api_key = settings.STRIPE_SECRET_KEY
 
 
def CreateCheckoutSessionView(request):
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        domain = "http://0.0.0.1:8000"
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
            success_url = domain + '/success/',
            cancel_url = domain + '/cancel/',
        )
        return redirect(checkout_session.url, code=303)
    else:
        return render(request, 'payment/procces.html', locals())
    

class SuccessView(TemplateView):
    template_name = "success.html"
 
class CancelView(TemplateView):
    template_name = "cancel.html"
