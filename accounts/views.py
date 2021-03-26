from django.shortcuts import render, redirect
from accounts.forms import LoginForm, SignUpForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from accounts.utils import send_to_email


def register_request(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            to_email = form.cleaned_data.get('email')
            send_to_email(request, user, to_email)

            messages.info(request, 'We are received a request to set your email.\n'
                                   'Please check your email box and click the link in the message.')
            return redirect('accounts:login')
        else:
            return render(request, 'accounts/register.html', {'register_form': form})
    form = SignUpForm
    return render(request, 'accounts/register.html', {'register_form': form})


def login_request(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    form = LoginForm()
    return render(request, 'accounts/login.html', {'login_form': form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('accounts:login')