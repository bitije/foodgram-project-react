from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(
        max_length=256,
        unique=True,
    )
    username = models.CharField(
        max_length=128,
        unique=True,
    )
    first_name = models.CharField(
        max_length=128,
    )
    last_name = models.CharField(
        max_length=128,
    )
    password = models.CharField(
        max_length=128,
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ('username',)

    def __str__(self) -> str:
        return f'{self.username}: {self.email}'


class Subscription(models.Model):
    author = models.ForeignKey(
        related_name='subscribers',
        to=CustomUser,
        on_delete=models.CASCADE,
    )
    follower = models.ForeignKey(
        related_name='subscriptions',
        to=CustomUser,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('author',)

    def __str__(self) -> str:
        return f'{self.follower.username} -> {self.author.username}'
