from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    pass


class Follow(models.Model):
    user = models.ForeignKey(
        CustomUser,
        related_name='followers',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        CustomUser,
        related_name='following',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.user.username} --> {self.author.username}'
