import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .api import user
from .api import organization
from .api import event
from .api import team
from .api import category
from .api import criteria
from .api import criteria_label
from .api import demo
from .api import demo_score


def index(request):
    """Landing page.

    If not logged in, then render page. Otherwise, redirect
    to the dashboard. Links to log in and register page.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'main/index.html')


def register(request):
    """Registration page for judges.

    Links to login page for users who already have an
    account. On successful registration, goes to profile
    page with a next to dashboard.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'GET':
        context = {}  # TODO: add form
        return render(request, 'registration/register.html')
    elif request.method == 'POST':
        # TODO: create and login user
        return redirect('dashboard')


@login_required
def profile(request):
    """Profile creation/edit page for judges."""
    if request.method == 'GET':
        context = {}  # TODO: add form
        return render(request, 'judge/profile.html')
    elif request.method == 'POST':
        # TODO: update user
        return redirect('profile')


@login_required
def dashboard(request):
    """Dashboard for judges.

    If not logged in, redirects to index. If logged in, but the
    profile is incomplete, redirect to profile. If logged in and
    the profile is complete, render page.

    """
    if request.method == 'GET':
        context = {}  # TODO: add context
        return render(request, 'judge/dashboard.html', context)


@login_required
def evaluate(request):
    """Form judges use to evaluate submissions.

    If not logged in, redirects to index. If logged in, but the
    profile is incomplete, redirect to profile. Otherwise, render
    the page. However, if judging has not started, disallow any
    form submissions.
    """
    if request.method == 'GET':
        context = {}  # TODO: add form
        return render(request, 'judge/evaluate.html')
    elif request.method == 'POST':
        # TODO: submit demo if judging is open
        return redirect('evaluate')
