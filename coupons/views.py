from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.utils import timezone
from cart.views import update_cart_in_all_user_sessions
from .models import Coupon
from .forms import CouponApplyForm


@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
            request.session['coupon_id'] = coupon.id
        except:
            request.session['coupon_id'] = None
        if request.user.is_authenticated:
            update_cart_in_all_user_sessions(request)
    return redirect('cart:cart_detail')
