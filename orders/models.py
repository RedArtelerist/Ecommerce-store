from decimal import Decimal

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from coupons.models import Coupon
from store.models import Product


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Preparing', 'Preparing'),
        ('Transferred to the carrier', 'Transferred to the carrier'),
        ('Delivering', 'Delivering'),
        ('Delivered to the department', 'Delivered to the department'),
        ('Received', 'Received'),
        ('Canceled', 'Canceled')
    )

    PAYMENT = (
        ('Cash', 'Cash'),
        ('Card', 'Card'),
        ('PayPal', 'PayPal'),
        ('PrivatPay', 'PrivatPay')
    )

    DELIVERY = (
        ('Courier', 'Courier'),
        ('Post office', 'Post office')
    )
    order_id = models.CharField(max_length=15)
    customer_first_name = models.CharField(max_length=20)
    customer_last_name = models.CharField(max_length=30)
    customer_phone = models.CharField(max_length=20)
    customer_email = models.EmailField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    city = models.CharField(max_length=100)
    address = models.CharField(max_length=250)

    status = models.CharField(max_length=40, choices=STATUS, default='New')
    delivery = models.CharField(max_length=15, choices=DELIVERY, default='Courier')
    paymentMethod = models.CharField(max_length=20, choices=PAYMENT, default='Cash')

    recipient_first_name = models.CharField(max_length=20)
    recipient_last_name = models.CharField(max_length=30)
    recipient_email = models.EmailField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    paid = models.BooleanField(default=False)

    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL,
                               related_name='orders', null=True, blank=True)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return 'Order {}'.format(self.order_id)

    def get_discount(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return round(total_cost * (self.discount / Decimal('100')))

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - self.get_discount()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price = models.PositiveIntegerField('Price')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

