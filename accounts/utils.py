from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models import Q
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from accounts.forms import UserPasswordResetForm


def send_to_email(request, user, to_email):
    current_site = get_current_site(request)
    mail_subject = 'Activate your account.'
    message = render_to_string('accounts/activation_request.html', {
        'user': user,
        'domain': current_site.domain,
        'protocol': 'https',
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Email was confirmed')
        return redirect('accounts:login')
    else:
        return render(request, 'accounts/activation_invalid.html')


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = UserPasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    current_site = get_current_site(request)
                    mail_subject = 'Password reset.'
                    message = render_to_string('accounts/password/password_reset_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'https',
                        'site_name': 'WayShop',
                    })
                    email = EmailMessage(
                        mail_subject, message, to=[data]
                    )
                    email.send()

                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                    return redirect('accounts:login')
            messages.error(request, 'An invalid email has been entered.')
            return render(request, "accounts/password/password_reset_form.html",
                          {"form": password_reset_form})

    password_reset_form = UserPasswordResetForm()
    return render(request, "accounts/password/password_reset_form.html",
                  {"form": password_reset_form})


def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user=user, data=request.POST)
            if form.is_valid():
                form.save()
                messages.info(request, "Thank you! Your password has been reset. Please log in below.")
                return redirect('accounts:login')
        else:
            form = SetPasswordForm(user=user)
        return render(request, 'accounts/password/password_reset_confirm.html', {
            'form': form,
        })
    else:
        return render(request, 'accounts/password/password_reset_invalid.html')