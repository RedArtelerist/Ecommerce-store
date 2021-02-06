from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404, render
from cart.views import update_cart_in_all_user_sessions
from store.models import Product, Category
from wishlist.wishlist import WishList


def wishlist_add(request, product_id):
    if request.user.is_authenticated:
        wishlist = WishList(request)
        product = get_object_or_404(Product, id=product_id)
        wishlist.add(product=product)
        update_cart_in_all_user_sessions(request)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return redirect('/')


def wishlist_remove(request, product_id):
    if request.user.is_authenticated:
        wishlist = WishList(request)
        product = get_object_or_404(Product, id=product_id)
        wishlist.remove(product)

        update_cart_in_all_user_sessions(request)
        return redirect('wishlist:wishlist_detail')

    return redirect('/')


def wishlist_detail(request):
    if request.user.is_authenticated:
        wishlist = WishList(request)

        return render(request, 'wishlist/detail.html', {'wishlist': wishlist})

    return redirect('/')


