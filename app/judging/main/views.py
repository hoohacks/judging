import json

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
    context = {
        'user': request.user
    }
    return render(request, 'main/index.html', context)


def register(request):
    """Registration page for judges.
    
    Links to login page for users who already have an
    account. On successful registration, goes to profile
    page with a next to dashboard.
    """
    return HttpResponse('Registration page')


def profile(request):
    """Profile creation/edit page for judges."""
    return HttpResponse('Profile update')


def dashboard(request):
    """Dashboard for judges.

    If not logged in, redirects to index. If logged in, but the
    profile is incomplete, redirect to profile. If logged in and
    the profile is complete, render page.
    
    """
    return HttpResponse('Judge dashboard')


def evaluate(request):
    """Form judges use to evaluate submissions.
    
    If not logged in, redirects to index. If logged in, but the
    profile is incomplete, redirect to profile. Otherwise, render
    the page. However, if judging has not started, disallow any
    form submissions.
    """
    return HttpResponse('Evaluation form')
