from django.forms.models import model_to_dict
from django.shortcuts import render


from ..models import Category
from ..api.team import Team
from ..api.user import User
from ..utils.api import *


def create(name: str,
           organization_id: int,
           description: str = None,
           number_winners: int = None,
           min_judges: int = None,
           is_opt_in: bool = None):
    kwargs = locals()
    fields = {
        'name': {'required': True, 'type': str},
        'organization_id': {'required': True, 'type': int},
        'description': {'required': False, 'type': str},
        'number_winners': {'required': False, 'type': int},
        'min_judges': {'required': False, 'type': int},
        'is_opt_in': {'required': False, 'type': bool},
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
        min_judges: int = None,
        is_opt_in: bool = None):
    kwargs = locals()
    fields = {
        'category_id': {'required': False, 'type': int},
        'name': {'required': False, 'type': str},
        'description': {'required': False, 'type': str},
        'organization_id': {'required': False, 'type': int},
        'number_winners': {'required': False, 'type': int},
        'min_judges': {'required': False, 'type': int},
        'is_opt_in': {'required': False, 'type': bool},
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
    if 'min_judges' in kwargs:
        categories = categories.filter(
            min_judges__exact=kwargs['min_judges'])
    if 'is_opt_in' in kwargs:
        categories = categories.filter(
            is_opt_in__exact=kwargs['is_opt_in'])
    return categories


def update(
        category_id: int,
        name: str = None,
        description: str = None,
        organization_id: int = None,
        number_winners: int = None,
        min_judges: int = None,
        is_opt_in: bool = None):
    kwargs = locals()
    fields = {
        'category_id': {'required': True, 'type': int},
        'name': {'required': False, 'type': str},
        'description': {'required': False, 'type': str},
        'organization_id': {'required': False, 'type': int},
        'number_winners': {'required': False, 'type': int},
        'min_judges': {'required': False, 'type': int},
        'is_opt_in': {'required': False, 'type': bool},
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
    team = Team.search(team_id=kwargs['team_id'])[0]
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
    team = Team.search(team_id=kwargs['team_id'])[0]
    category.submissions.remove(team)
    return category


def add_judge(category_id: int,
              judge_id: int):
    kwargs = locals()
    fields = {
        'category_id': {'required': True, 'type': int},
        'judge_id': {'required': True, 'type': int},
    }
    kwargs = clean_fields(fields, kwargs)

    category = Category.objects.get(pk=kwargs['category_id'])
    judge = User.search(user_id=kwargs['judge_id'], is_judge=True)[0]
    category.judges.add(judge)
    return category


def remove_judge(category_id: int,
                 judge_id: int):
    kwargs = locals()
    fields = {
        'category_id': {'required': True, 'type': int},
        'judge_id': {'required': True, 'type': int},
    }
    kwargs = clean_fields(fields, kwargs)

    category = Category.objects.get(pk=kwargs['category_id'])
    judge = User.search(user_id=kwargs['judge_id'], is_judge=True)[0]
    category.judges.remove(judge)
    return category
