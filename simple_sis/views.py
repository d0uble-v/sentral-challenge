from django.shortcuts import render, redirect, resolve_url
from django.http import Http404
from django.contrib.auth import (
    authenticate,
    login as django_login,
    logout as django_logout,
)
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Activity, ActivityAttendee


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
        'h1_title': 'School Activities',
        'user': user,
        'activities': activities,
    }

    return render(request, 'home.html', context)


@login_required
def view_activity(request, id):
    user = request.user
    try:
        activity = user.school.activities.get(id=id)
    except Activity.DoesNotExist:
        raise Http404("Activity does not exist")

    context = {
        'page_title': f'Activity - {activity.name}',
        'h1_title': f'{activity.name}',
        'user': user,
        'activity': activity,
        # Normally this would be done with a reverse lookup
        # but for the save of the challenge we can run a
        # raw SQL query
        'organisers': activity.attendees.filter(is_organiser=True),
        'attendees': activity.attendees.filter(is_organiser=False),
    }

    return render(request, 'activity-view.html', context)