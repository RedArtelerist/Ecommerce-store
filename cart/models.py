from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db import models
from jsonfield import JSONField


class UserCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    modification_date = models.DateTimeField(auto_now=True)
    items_cart = JSONField()
    coupon = models.PositiveIntegerField()
    items_wishlist = JSONField()
    chat_id = models.PositiveIntegerField(default=0)
    message_id = models.IntegerField(default=-1)


class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)