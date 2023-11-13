from celery import shared_task
import requests


@shared_task
def get_exchange_rate():
    access_key = '237444eb25ac18c4575369adc57044ae'
    base_currency = 'USD'
    target_currency = 'RUB'
    url_api = 'http://api.currencylayer.com/'
    url = f'{url_api}live?access_key={access_key}&source={base_currency}&currencies={target_currency}'

    response = requests.get(url)
    data = response.json()

    if 'quotes' in data:
        exchange_rate = data['quotes'][f'{base_currency}{target_currency}']
        return exchange_rate

    return None
