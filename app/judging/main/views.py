import json

from django.shortcuts import render

from .api.user import *
from . import testpage


def test_page(request):
    return render(request, 'micro/api.html', testpage.context)
