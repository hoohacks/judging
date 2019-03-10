from django.forms.models import model_to_dict
from django.shortcuts import render


from ..models import Organization
from ..utils.api import *


def organization_create(request):
    check_method(request, 'POST')
    fields = {
        'name': {'required': True, 'type': str},
    }
    kwargs = extract_fields(fields, request.POST)
    organization = Organization.objects.create(**kwargs)
    return JsonResponse(model_to_dict(organization))


def organization_search(request):
    check_method(request, 'GET')
    fields = {
        'organization_id': {'required': False, 'type': int},
        'name': {'required': False, 'type': str},
    }
    kwargs = extract_fields(fields, request.GET)

    organizations = Organization.objects.all()
    if 'organization_id' in kwargs:
        organizations = organizations.filter(pk=kwargs['organization_id'])
    if 'name' in kwargs:
        organizations = organizations.filter(name__iexact=kwargs['name'])

    results = {
        'results': [model_to_dict(organization) for organization in organizations]
    }
    return JsonResponse(results)


def organization_update(request):
    check_method(request, 'POST')
    fields = {
        'organization_id': {'required': True, 'type': int},
        'name': {'required': False, 'type': str},
    }
    kwargs = extract_fields(fields, request.POST)

    organization_id = kwargs.pop('organization_id')
    Organization.objects.filter(pk=organization_id).update(**kwargs)
    organization = Organization.objects.get(pk=organization_id)
    return JsonResponse(model_to_dict(organization))


def organization_delete(request):
    check_method(request, 'POST')
    fields = {
        'organization_id': {'required': True, 'type': int},
    }
    kwargs = extract_fields(fields, request.POST)

    Organization.objects.get(pk=kwargs['organization_id']).delete()
    return JsonResponse({})
