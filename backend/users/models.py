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
