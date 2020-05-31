from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


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
                error = {'error_log_div': 'Your account was inactive.'}
                return render(request, 'UsersActions/login.html', error)
        else:
            error = {'error_log_div': 'Invalid login details given.'}
            return render(request, 'UsersActions/login.html', error)
    else:
        return render(request, 'UsersActions/login.html')


@login_required
def my_logout(request):
    logout(request)
    return render(request, 'UsersActions/logout.html')
