from django.forms.models import model_to_dict
from django.shortcuts import render


from ..models import Category, Team
from ..utils.api import *


def create(name: str,
                    organization_id: int,
                    description: str = None,
                    number_winners: int = None,
                    is_opt_in: bool = None,
                    can_anyone_judge: bool = None):
    kwargs = locals()
    fields = {
        'name': {'required': True, 'type': str},
        'organization_id': {'required': True, 'type': int},
        'description': {'required': False, 'type': str},
        'number_winners': {'required': False, 'type': int},
        'is_opt_in': {'required': False, 'type': bool},
        'can_anyone_judge': {'required': False, 'type': bool},
    }
    kwargs = clean_fields(fields, kwargs)
    category = Category.objects.create(**kwargs)
    return category


def search(
        category_id: int = None,
        name: str = None,
        description: str = None,
        organization_id: int = None,
        number_winners: int = None,
        is_opt_in: bool = None,
        can_anyone_judge: bool = None):
    kwargs = locals()
    fields = {
        'category_id': {'required': False, 'type': int},
        'name': {'required': False, 'type': str},
        'description': {'required': False, 'type': str},
        'organization_id': {'required': False, 'type': int},
        'number_winners': {'required': False, 'type': int},
        'is_opt_in': {'required': False, 'type': bool},
        'can_anyone_judge': {'required': False, 'type': bool},
    }
    kwargs = clean_fields(fields, kwargs)

    categories = Category.objects.all()
    if 'category_id' in kwargs:
        categories = categories.filter(pk=kwargs['category_id'])
    if 'name' in kwargs:
        categories = categories.filter(name__icontains=kwargs['name'])
    if 'description' in kwargs:
        categories = categories.filter(
            description__icontains=kwargs['description'])
    if 'organization_id' in kwargs:
        categories = categories.filter(
            organization__id__exact=kwargs['organization_id'])
    if 'number_winners' in kwargs:
        categories = categories.filter(
            number_winners__exact=kwargs['number_winners'])
    if 'is_opt_in' in kwargs:
        categories = categories.filter(
            is_opt_in__exact=kwargs['is_opt_in'])
    if 'can_anyone_judge' in kwargs:
        categories = categories.filter(
            can_anyone_judge__exact=kwargs['can_anyone_judge'])
    return categories


def update(
        category_id: int,
        name: str = None,
        description: str = None,
        organization_id: int = None,
        number_winners: int = None,
        is_opt_in: bool = None,
        can_anyone_judge: bool = None):
    kwargs = locals()
    fields = {
        'category_id': {'required': True, 'type': int},
        'name': {'required': False, 'type': str},
        'description': {'required': False, 'type': str},
        'organization_id': {'required': False, 'type': int},
        'number_winners': {'required': False, 'type': int},
        'is_opt_in': {'required': False, 'type': bool},
        'can_anyone_judge': {'required': False, 'type': bool},
    }
    kwargs = clean_fields(fields, kwargs)

    category_id = kwargs.pop('category_id')
    Category.objects.filter(pk=category_id).update(**kwargs)
    category = Category.objects.get(pk=category_id)
    return category


def delete(category_id: int):
    kwargs = locals()
    fields = {
        'category_id': {'required': True, 'type': int},
    }
    kwargs = clean_fields(fields, kwargs)

    Category.objects.get(pk=kwargs['category_id']).delete()


def add_team(category_id: int,
                      team_id: int):
    kwargs = locals()
    fields = {
        'category_id': {'required': True, 'type': int},
        'team_id': {'required': True, 'type': int},
    }
    kwargs = clean_fields(fields, kwargs)

    category = Category.objects.get(pk=kwargs['category_id'])
    team = Team.objects.get(pk=kwargs['team_id'])
    category.submissions.add(team)
    return category


def remove_team(category_id: int,
                         team_id: int):
    kwargs = locals()
    fields = {
        'category_id': {'required': True, 'type': int},
        'team_id': {'required': True, 'type': int},
    }
    kwargs = clean_fields(fields, kwargs)

    category = Category.objects.get(pk=kwargs['category_id'])
    team = Team.objects.get(pk=kwargs['team_id'])
    category.submissions.remove(team)
    return category
