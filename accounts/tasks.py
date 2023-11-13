from celery import shared_task
from django.core.mail import send_mail
from goods.models import Product
from .models import Follow, CustomUser


@shared_task
def send_product_list(user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        subscribers = Follow.objects.filter(author=user)
        for i in subscribers:
            send_mail(
                'Product List',
                user.username,
                '123@yandex.com',
                [{i.user.email}]
            )
    except CustomUser.DoesNotExist:
        print(f"User with ID {user_id} does not exist")
