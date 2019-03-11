from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse


def index(request):
    """Landing page with links to register and login"""
    if request.method == 'GET':
        # get authentication information
        # if is logged in
        #   redirect to dashboard
        # else
        #   get event information
        #   display main page
        context = {
            'is_logged_in': False
        }
        return render(request, 'main/index.html', context)
    else:
        return HttpResponseRedirect(reverse('web:index'))
