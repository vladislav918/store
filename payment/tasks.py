from celery import shared_task
from django.core.mail import send_mail
from accounts.models import CustomUser


@shared_task
def payment_completed(user_email):
    try:
        send_mail(
            'Thanks',
            'Thank you for buying in our store',
            '123@yandex.com',
            [user_email],
        )
    except CustomUser.DoesNotExist:
        print(f"User {user_email} does not exist")
