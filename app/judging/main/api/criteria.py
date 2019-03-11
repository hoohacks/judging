from django.forms.models import model_to_dict
from django.shortcuts import render


from ..models import Criteria
from ..utils.api import *


def criteria_create(request):
    check_method(request, 'POST')
    fields = {
        'name': {'required': True, 'type': str},
        'description': {'required': False, 'type': str},
        'min_score': {'required': False, 'type': int},
        'max_score': {'required': False, 'type': int},
        'weight': {'required': False, 'type': float},
    }
    kwargs = extract_fields(fields, request.POST)
    criteria = Criteria.objects.create(**kwargs)
    return JsonResponse(model_to_dict(criteria))


def criteria_search(request):
    check_method(request, 'GET')
    fields = {
        'criteria_id': {'required': False, 'type': int},
        'name': {'required': False, 'type': str},
        'description': {'required': False, 'type': str},
    }
    kwargs = extract_fields(fields, request.GET)

    criterias = Criteria.objects.all()
    if 'criteria_id' in kwargs:
        criterias = criterias.filter(pk=kwargs['criteria_id'])
    if 'name' in kwargs:
        criterias = criterias.filter(name__iexact=kwargs['name'])
    if 'description' in kwargs:
        criterias = criterias.filter(
            description__icontains=kwargs['description'])

    results = {
        'results': [model_to_dict(criteria) for criteria in criterias]
    }
    return JsonResponse(results)


def criteria_update(request):
    check_method(request, 'POST')
    fields = {
        'criteria_id': {'required': True, 'type': int},
        'name': {'required': False, 'type': str},
        'description': {'required': False, 'type': str},
        'min_score': {'required': False, 'type': int},
        'max_score': {'required': False, 'type': int},
        'weight': {'required': False, 'type': float},
    }
    kwargs = extract_fields(fields, request.POST)

    criteria_id = kwargs.pop('criteria_id')
    Criteria.objects.filter(pk=criteria_id).update(**kwargs)
    criteria = Criteria.objects.get(pk=criteria_id)
    return JsonResponse(model_to_dict(criteria))


def criteria_delete(request):
    check_method(request, 'POST')
    fields = {
        'criteria_id': {'required': True, 'type': int},
    }
    kwargs = extract_fields(fields, request.POST)

    Criteria.objects.get(pk=kwargs['criteria_id']).delete()
    return JsonResponse({})
