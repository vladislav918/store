from .tasks import get_exchange_rate


def currency(request):
    return {'exchange_rate': get_exchange_rate}
