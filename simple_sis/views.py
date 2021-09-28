from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth import (
    authenticate,
    login as django_login,
    logout as django_logout,
)
from django.contrib.auth.decorators import login_required
from django.conf import settings


def login(request):
    ''''''
    context = {'page_title': 'Log In'}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            django_login(request, user)
            return redirect(
                request.GET.get(
                    'next', resolve_url(settings.LOGIN_REDIRECT_URL)
                )
            )

    return render(request, 'login.html', context)


@login_required
def logout(request):
    django_logout(request)
    return redirect(resolve_url(settings.LOGOUT_REDIRECT_URL))


@login_required
def home(request):
    ''''''
    user = request.user
    activities = user.school.activities.all()

    context = {
        'page_title': 'Home',
        'user': user,
        'activities': activities,
    }

    return render(request, 'home.html', context)
