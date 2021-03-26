from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from cart.cart import Cart
from cart.views import update_cart_in_all_user_sessions
from orders.forms import OrderCreateForm
from orders.models import OrderItem
from orders.utils import unique_order_id


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            if len(cart) == 0:
                return redirect('/')

            #check payment method
            order = form.save(commit=False)
            order_id = unique_order_id()
            if request.user.is_authenticated:
                order.user = request.user

            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount

            order.order_id = order_id
            order.save()

            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            request.session['coupon_id'] = None

            if request.user.is_authenticated:
                update_cart_in_all_user_sessions(request)

            return render(request, 'orders/created.html', {'order': order})

    form = OrderCreateForm(use_required_attribute=False, initial={'city': 'Киев'})
    if len(cart) == 0:
        return redirect('cart:cart_detail')

    return render(request, 'orders/checkout.html', {'form': form})