from django.forms.models import model_to_dict
from django.shortcuts import render


from ..models import Organization
from ..utils.api import *


def create(name: str):
    kwargs = locals()
    fields = {
        'name': {'required': True, 'type': str},
    }
    kwargs = clean_fields(fields, kwargs)
    organization = Organization.objects.create(**kwargs)
    return organization


def search(organization_id: int = None, name: str = None):
    kwargs = locals()
    fields = {
        'organization_id': {'required': False, 'type': int},
        'name': {'required': False, 'type': str},
    }
    kwargs = clean_fields(fields, kwargs)

    organizations = Organization.objects.all()
    if 'organization_id' in kwargs:
        organizations = organizations.filter(pk=kwargs['organization_id'])
    if 'name' in kwargs:
        organizations = organizations.filter(name__iexact=kwargs['name'])
    return organizations


def update(organization_id: int, name: str = None):
    kwargs = locals()
    fields = {
        'organization_id': {'required': True, 'type': int},
        'name': {'required': False, 'type': str},
    }
    kwargs = clean_fields(fields, kwargs)

    organization_id = kwargs.pop('organization_id')
    Organization.objects.filter(pk=organization_id).update(**kwargs)
    organization = Organization.objects.get(pk=organization_id)
    return organization


def delete(organization_id: int):
    kwargs = locals()
    fields = {
        'organization_id': {'required': True, 'type': int},
    }
    kwargs = clean_fields(fields, kwargs)

    Organization.objects.get(pk=kwargs['organization_id']).delete()
