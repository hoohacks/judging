from django.forms.models import model_to_dict
from django.shortcuts import render


from ..models import User, Organization
from ..utils.api import *


def user_create(request):
    check_method(request, 'POST')
    fields = {
        'first_name': {'required': True, 'type': str},
        'last_name': {'required': True, 'type': str},
        'username': {'required': True, 'type': str},
        'password': {'required': True, 'type': str},
        'is_staff': {'required': False, 'type': bool},
        'organization_id': {'required': True, 'type': int},
    }
    kwargs = extract_fields(fields, request.POST)
    organization_id = kwargs.pop('organization_id')
    organization = Organization.objects.get(pk=organization_id)
    kwargs['organization'] = organization
    user = User.objects.create_user(**kwargs)
    return JsonResponse(model_to_dict(user))


def user_search(request):
    check_method(request, 'GET')
    fields = {
        'user_id': {'required': False, 'type': int},
        'username': {'required': False, 'type': str},
        'is_staff': {'required': False, 'type': bool},
        'organization_id': {'required': False, 'type': int},
    }
    kwargs = extract_fields(fields, request.GET)

    users = User.objects.all()
    if 'user_id' in kwargs:
        users = users.filter(pk=kwargs['user_id'])
    if 'username' in kwargs:
        users = users.filter(username__iexact=kwargs['username'])
    if 'is_staff' in kwargs:
        users = users.filter(username__iexact=kwargs['is_staff'])
    if 'organization_id' in kwargs:
        users = users.filter(organization__id__exact=kwargs['organization_id'])

    results = {
        'results': [model_to_dict(user) for user in users]
    }
    return JsonResponse(results)


def user_update(request):
    check_method(request, 'POST')
    fields = {
        'user_id': {'required': True, 'type': int},
        'username': {'required': False, 'type': str},
        'is_staff': {'required': False, 'type': bool},
        'organization_id': {'required': False, 'type': int},
    }
    kwargs = extract_fields(fields, request.POST)

    if 'organization_id' in kwargs:
        organization_id = kwargs.pop('organization_id')
        organization = Organization.objects.get(pk=organization_id)
        kwargs['organization'] = organization

    User.objects.filter(pk=kwargs['user_id']).update(**kwargs)
    user = User.objects.get(pk=kwargs['user_id'])
    return JsonResponse(model_to_dict(user))


def user_delete(request):
    check_method(request, 'POST')
    fields = {
        'user_id': {'required': True, 'type': int},
    }
    kwargs = extract_fields(fields, request.POST)

    User.objects.get(pk=kwargs['user_id']).delete()
    return JsonResponse({})
