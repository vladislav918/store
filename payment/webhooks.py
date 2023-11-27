from django.views.decorators.csrf import csrf_exempt
import stripe
from django.conf import settings
from orders.models import Order
from django.http import HttpResponse
from cart.cart import Cart
from .tasks import payment_completed


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET)
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        order_id = session['metadata']['order_id']
        order = Order.objects.get(id=order_id)
        order.paid = True
        order.save()
        payment_completed.delay(session['customer_details']['email'])

    return HttpResponse(status=200)
