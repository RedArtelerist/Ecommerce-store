import json
from django.contrib.sessions.backends.db import SessionStore
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from wishlist.wishlist import WishList
from .cart import Cart
from .forms import CartAddProductForm
from store.models import Product
from .models import UserSession


def update_cart_in_all_user_sessions(request):
    user_sessions = UserSession.objects.filter(user=request.user).\
        exclude(session__session_key=request.session.session_key)

    user_cart = Cart(request)
    user_wishlist = WishList(request)

    if user_sessions:
        for user_session in user_sessions:
            session = user_session.session
            session_data = session.get_decoded()
            session_data['cart'] = user_cart.cart
            session_data['wishlist'] = user_wishlist.wishlist
            encoded_data = SessionStore().encode(session_data)
            session.session_data = encoded_data
            session.save()


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    if product.available:
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product,
                     quantity=cd['quantity'],
                     update_quantity=cd['update'])
        if request.user.is_authenticated:
            update_cart_in_all_user_sessions(request)

        return redirect('cart:cart_detail')


@csrf_exempt
@require_POST
def cart_update(request):
    data = json.loads(request.body)
    cart = Cart(request)

    product_id = data['productId']
    action = data['action']
    product = get_object_or_404(Product, id=product_id)

    if product.available:
        if action == 'add':
            cart.add(product=product,
                     quantity=1)
        if action == 'del':
            cart.remove_single(product)
        if request.user.is_authenticated:
            update_cart_in_all_user_sessions(request)

        return JsonResponse('Cart updated', safe=False)


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    if request.user.is_authenticated:
        update_cart_in_all_user_sessions(request)

    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})
