from django.forms.models import model_to_dict
from django.shortcuts import render


from ..models import Demo, Team, User
from ..utils.api import *


def demo_create(request):
    check_method(request, 'POST')
    fields = {
        'judge_id': {'required': True, 'type': int},
        'team_id': {'required': True, 'type': int},
    }
    kwargs = extract_fields(fields, request.POST)
    demo = Demo.objects.create(**kwargs)
    return JsonResponse(model_to_dict(demo))


def demo_search(request):
    check_method(request, 'GET')
    fields = {
        'demo_id': {'required': False, 'type': int},
        'judge_id': {'required': False, 'type': int},
        'team_id': {'required': False, 'type': int},
    }
    kwargs = extract_fields(fields, request.GET)

    demos = Demo.objects.all()
    if 'demo_id' in kwargs:
        demos = demos.filter(pk=kwargs['demo_id'])
    if 'judge_id' in kwargs:
        demos = demos.filter(judge__id__exact=kwargs['judge_id'])
    if 'team_id' in kwargs:
        demos = demos.filter(team__id__exact=kwargs['team_id'])

    results = {
        'results': [model_to_dict(demo) for demo in demos]
    }
    return JsonResponse(results)


def demo_update(request):
    check_method(request, 'POST')
    fields = {
        'demo_id': {'required': True, 'type': int},
        'judge_id': {'required': False, 'type': int},
        'team_id': {'required': False, 'type': int},
    }
    kwargs = extract_fields(fields, request.POST)

    demo_id = kwargs.pop('demo_id')
    Demo.objects.filter(pk=demo_id).update(**kwargs)
    demo = Demo.objects.get(pk=demo_id)
    return JsonResponse(model_to_dict(demo))


def demo_delete(request):
    check_method(request, 'POST')
    fields = {
        'demo_id': {'required': True, 'type': int},
    }
    kwargs = extract_fields(fields, request.POST)

    Demo.objects.get(pk=kwargs['demo_id']).delete()
    return JsonResponse({})
