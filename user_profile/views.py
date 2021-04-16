from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from orders.models import Order
from user_profile.filter import OrderFilter
from user_profile.forms import ProfileForm, UserForm, PasswordChangingForm, ChangeUserNameForm


@login_required
def personal_info(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile:personal_info')
        else:
            messages.error(request, 'Please correct the error below.')

    user_form = UserForm()
    profile_form = ProfileForm()
    return render(request, 'user_profile/personal_info.html',
                  {'title': 'Personal info',
                   'user_form': user_form,
                   'profile_form': profile_form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangingForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile:change_password')
        else:
            messages.error(request, 'Your old password is incorrect')
            return redirect('profile:change_password')
    else:
        form = PasswordChangingForm(request.user)
    return render(request, 'user_profile/change_password.html', {
        'title': 'Change password',
        'form': form
    })


@login_required
def account_settings(request):
    if request.method == 'POST':
        form = ChangeUserNameForm(request.POST, instance=request.user)
        username = form.data['username']
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile:account_settings')
        else:
            print(form.errors)
            messages.error(request, f'Username "{username}" is not available.')
            return redirect('profile:account_settings')

    form = ChangeUserNameForm()
    return render(request, 'user_profile/account_settings.html', {
        'title': 'Account settings',
        'form': form,
    })


@require_POST
@login_required
def delete_account(request):
    user = request.user
    user.delete()
    return redirect('/')


@login_required
def orders(request):
    orders = request.user.order_set.all()

    f = OrderFilter(request.GET, queryset=orders)
    return render(request, 'user_profile/user_orders.html', {
        'title': 'Orders',
        'filter': f,
        'orders': f.qs})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)

    return render(request, 'user_profile/order_detail.html', {
        'title': 'Order detail',
        'order': order
    })


@require_POST
@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    order.status = 'Canceled'
    order.save()
    return redirect('profile:order_detail', order_id)