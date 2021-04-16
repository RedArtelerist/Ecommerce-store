from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

from store.models import Product
from wishlist.wishlist import WishList
from .cart import Cart
from .models import *


@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    UserSession.objects.get_or_create(user=user, session_id=request.session.session_key)


@receiver(user_logged_in)
def get_user_cart(sender, user, request, **kwargs):
    try:
        print("Login")
        user_cart = UserCart.objects.get(user=user)

        cart = Cart(request)
        wishlist = WishList(request)
        if not cart.is_empty:
            print(cart)

        cart_items = dict(user_cart.items_cart)
        wishlist_items = dict(user_cart.items_wishlist)

        for key, value in cart_items.items():
            product = Product.objects.get(pk=key)
            if product and product.available:
                cart.add(product, quantity=value['quantity'], price=value['price'])

        for key in wishlist_items.keys():
            product = Product.objects.get(pk=key)
            wishlist.add(product)

        if user_cart.coupon != 0:
            request.session['coupon_id'] = user_cart.coupon
        else:
            request.session['coupon_id'] = None

    except UserCart.DoesNotExist:
        print("Except")
        user_cart = UserCart.objects.create(user=user, coupon=0)
        request.session['coupon_id'] = None
    if not user_cart:
        print("Cart is absent")


@receiver(user_logged_out)
def create_or_update_user_cart(sender, request, user, **kwargs):
    user_cart = UserCart.objects.get_or_create(user=user)[0]
    cart = Cart(request)
    wishlist = WishList(request)
    user_cart.items_cart = cart.cart.items()
    try:
        if request.session['coupon_id'] is not None:
            user_cart.coupon = request.session['coupon_id']
        else:
            user_cart.coupon = 0
    except Exception:
        user_cart.coupon = 0

    user_cart.items_wishlist = wishlist.wishlist.items()
    user_cart.save()