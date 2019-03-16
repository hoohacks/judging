from django.forms.models import model_to_dict
from django.shortcuts import render


from ..models import User
from ..api import organization as Organization
from ..api import category as Category
from ..api import event as Event
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
    organization = Organization.search(organization_id=organization_id)[0]
    kwargs['organization'] = organization
    user = User.objects.create_user(**kwargs)

    # Add judge to category by default
    organizers_id = Event.get().organizers.id
    for category in Category.search():
        if category.organization.id == organizers_id or (user.organization.id and (category.organization.id == user.organization.id)):
            Category.add_judge(category.id, user.id)
    return user


def search(user_id: int = None,
           first_name: str = None,
           last_name: str = None,
           username: str = None,
           organization_id: int = None,
           is_staff: bool = None,
           is_judge: bool = None):
    kwargs = locals()
    fields = {
        'user_id': {'required': False, 'type': int},
        'username': {'required': False, 'type': str},
        'first_name': {'required': False, 'type': str},
        'last_name': {'required': False, 'type': str},
        'is_staff': {'required': False, 'type': bool},
        'is_judge': {'required': False, 'type': bool},
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
    if 'is_judge' in kwargs:
        users = users.filter(organization__isnull=False)
        users = users.filter(is_staff__exact=False)

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
    user_id = kwargs.pop('user_id')
    User.objects.filter(pk=user_id).update(**kwargs)
    user = User.objects.get(pk=user_id)

    # Add judge to category by default
    user.categories.clear()
    organizers_id = Event.get().organizers.id
    for category in Category.search():
        if category.organization.id == organizers_id or (user.organization.id and (category.organization.id == user.organization.id)):
            Category.add_judge(category.id, user.id)
    return user


def delete(user_id: int):
    kwargs = locals()
    fields = {
        'user_id': {'required': True, 'type': int},
    }
    kwargs = clean_fields(fields, kwargs)

    User.objects.get(pk=kwargs['user_id']).delete()
