from django.shortcuts import render
from .tasks import get_exchange_rate


def exchange_rate_view(request):
    exchange_rate = get_exchange_rate()

    context = {
        'live': exchange_rate
    }

    return render(request, 'converter/live.html', context)
