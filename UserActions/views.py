from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from UserActions.tokens import account_activation_token
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from UserActions.forms import UserForm


def my_login(request):
    if request.method == 'POST':
        username = request.POST.get('login')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return render(request, 'index.html')
            else:
                error = {'error_log_div': 'Twoje konto jest nieaktywne.'}
                # error = {'error_log_div': 'Your account was inactive.'}
                return render(request, 'UsersActions/login.html', error)
        else:
            error = {'error_log_div': 'Nieprawidłowe dane logowania.'}
            # error = {'error_log_div': 'Invalid login details given.'}
            return render(request, 'UsersActions/login.html', error)
    else:
        return render(request, 'UsersActions/login.html')


@login_required
def my_logout(request):
    logout(request)
    return render(request, 'UsersActions/logout.html')


def account_activation_sent(request):
    return render(request, 'users/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.userprofile.email_confirmed = True
        user.save()
        login(request, user)
        return render(request, 'users/account_activation_valid.html')
    else:
        return render(request, 'users/account_activation_invalid.html')


def register(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.is_active = False
            user.set_password(user.password)
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('UsersActions/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': force_text(urlsafe_base64_encode(force_bytes(user.pk))),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('UsersActions/account_activation_sent')
    else:
        user_form = UserForm()
    return render(request, 'UsersActions/login.html', {'user_form': user_form})