import json

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
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
from .forms.registration import RegistrationForm
from .forms.profile import UpdateProfileForm


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
        context = {'form': RegistrationForm()}
        return render(request, 'registration/register.html', context)
    elif request.method == 'POST':
        form = RegistrationForm(request.POST)
        if not form.is_valid():
            redirect('register')
        form.save()  # create user
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('dashboard')
    return redirect('register')


@login_required
def profile(request):
    """Profile creation/edit page for judges."""
    if request.method == 'GET':
        context = {'form': UpdateProfileForm(instance=request.user)}  # TODO: add form
        return render(request, 'judge/profile.html', context)
    elif request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        context = {'form': form}
        return render(request, 'judge/profile.html', context)


@login_required
def dashboard(request):
    """Dashboard for judges.

    If not logged in, redirects to index. If logged in, but the
    profile is incomplete, redirect to profile. If logged in and
    the profile is complete, render page.

    """
    if not request.user.is_profile_complete():
        return redirect('profile')

    if request.method == 'GET':
        context = {
            'user': request.user,
            'demo_queue': [],
            'past_demos': [],
        }
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
