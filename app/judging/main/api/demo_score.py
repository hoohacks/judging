from django.forms.models import model_to_dict
from django.shortcuts import render


from ..models import DemoScore, Team, User
from ..utils.api import *


def demo_score_create(request):
    check_method(request, 'POST')
    fields = {
        'demo_id': {'required': True, 'type': int},
        'criteria_id': {'required': True, 'type': int},
        'value': {'required': True, 'type': int},
    }
    kwargs = extract_fields(fields, request.POST)
    demo_score = DemoScore.objects.create(**kwargs)
    return JsonResponse(model_to_dict(demo_score))


def demo_score_search(request):
    check_method(request, 'GET')
    fields = {
        'demo_score_id': {'required': False, 'type': int},
        'demo_id': {'required': False, 'type': int},
        'criteria_id': {'required': False, 'type': int},
        'value': {'required': False, 'type': int},
    }
    kwargs = extract_fields(fields, request.GET)

    demo_scores = DemoScore.objects.all()
    if 'demo_score_id' in kwargs:
        demo_scores = demo_scores.filter(pk=kwargs['demo_score_id'])
    if 'demo_id' in kwargs:
        demo_scores = demo_scores.filter(demo__id__exact=kwargs['demo_id'])
    if 'criteria_id' in kwargs:
        demo_scores = demo_scores.filter(
            criteria__id__exact=kwargs['criteria_id'])
    if 'value' in kwargs:
        demo_scores = demo_scores.filter(value__exact=kwargs['value'])

    results = {
        'results': [model_to_dict(demo_score) for demo_score in demo_scores]
    }
    return JsonResponse(results)


def demo_score_update(request):
    check_method(request, 'POST')
    fields = {
        'demo_score_id': {'required': True, 'type': int},
        'demo_id': {'required': False, 'type': int},
        'criteria_id': {'required': False, 'type': int},
        'value': {'required': False, 'type': int},
    }
    kwargs = extract_fields(fields, request.POST)

    demo_score_id = kwargs.pop('demo_score_id')
    DemoScore.objects.filter(pk=demo_score_id).update(**kwargs)
    demo_score = DemoScore.objects.get(pk=demo_score_id)
    return JsonResponse(model_to_dict(demo_score))


def demo_score_delete(request):
    check_method(request, 'POST')
    fields = {
        'demo_score_id': {'required': True, 'type': int},
    }
    kwargs = extract_fields(fields, request.POST)

    DemoScore.objects.get(pk=kwargs['demo_score_id']).delete()
    return JsonResponse({})
