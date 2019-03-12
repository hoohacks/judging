from django.forms.models import model_to_dict
from django.shortcuts import render


from ..models import User, Organization
from ..utils.api import *


def create(
    first_name: str,
    last_name: str,
    username: str,
    password: str,
    organization_id: int = None,
    is_staff: bool = None,
    is_superuser: bool = None,
):
    kwargs = locals()
    fields = {
        'first_name': {'required': True, 'type': str},
        'last_name': {'required': True, 'type': str},
        'username': {'required': True, 'type': str},
        'password': {'required': True, 'type': str},
        'organization_id': {'required': False, 'type': int},
        'is_staff': {'required': False, 'type': bool},
        'is_superuser': {'required': False, 'type': bool},
    }
    kwargs = clean_fields(fields, kwargs)
    organization_id = kwargs.pop('organization_id')
    organization = Organization.objects.get(pk=organization_id)
    kwargs['organization'] = organization
    user = User.objects.create_user(**kwargs)
    return user


def search(user_id: int = None,
           first_name: str = None,
           last_name: str = None,
           username: str = None,
           organization_id: int = None,
           is_staff: bool = None):
    kwargs = locals()
    fields = {
        'user_id': {'required': False, 'type': int},
        'username': {'required': False, 'type': str},
        'first_name': {'required': False, 'type': str},
        'last_name': {'required': False, 'type': str},
        'is_staff': {'required': False, 'type': bool},
        'organization_id': {'required': False, 'type': int},
    }
    kwargs = clean_fields(fields, kwargs)

    users = User.objects.all()
    if 'user_id' in kwargs:
        users = users.filter(pk=kwargs['user_id'])
    if 'username' in kwargs:
        users = users.filter(username__icontains=kwargs['username'])
    if 'first_name' in kwargs:
        users = users.filter(first_name__icontains=kwargs['first_name'])
    if 'last_name' in kwargs:
        users = users.filter(last_name__icontains=kwargs['last_name'])
    if 'is_staff' in kwargs:
        users = users.filter(is_staff__exact=kwargs['is_staff'])
    if 'organization_id' in kwargs:
        users = users.filter(organization__id__exact=kwargs['organization_id'])

    return users


def update(user_id: int,
           first_name: str = None,
           last_name: str = None,
           username: str = None,
           organization_id: int = None,
           is_staff: bool = None):
    kwargs = locals()
    fields = {
        'user_id': {'required': True, 'type': int},
        'username': {'required': False, 'type': str},
        'first_name': {'required': False, 'type': str},
        'last_name': {'required': False, 'type': str},
        'is_staff': {'required': False, 'type': bool},
        'organization_id': {'required': False, 'type': int},
    }
    kwargs = clean_fields(fields, kwargs)
    User.objects.filter(pk=kwargs['user_id']).update(**kwargs)
    user = User.objects.get(pk=kwargs['user_id'])
    return user


def delete(user_id: int):
    kwargs = locals()
    fields = {
        'user_id': {'required': True, 'type': int},
    }
    kwargs = clean_fields(fields, kwargs)

    User.objects.get(pk=kwargs['user_id']).delete()
