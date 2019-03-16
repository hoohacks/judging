from django.forms.models import model_to_dict
from django.shortcuts import render


from ..models import Team
from ..utils.api import *


def create(name: str,
           table: str = None,
           members: str = None,
           link: str = None,
           is_anchor: bool = None):
    """Create new team or break if already exists."""
    kwargs = locals()
    fields = {
        'name': {'required': True, 'type': str},
        'table': {'required': False, 'type': str},
        'members': {'required': False, 'type': str},
        'link': {'required': False, 'type': str},
        'is_anchor': {'required': False, 'type': bool},
    }
    kwargs = clean_fields(fields, kwargs)
    team = Team.objects.create(**kwargs)
    return team


def search(team_id: int = None,
           name: str = None,
           table: str = None,
           members: str = None,
           link: str = None,
           is_anchor: bool = None):
    kwargs = locals()
    fields = {
        'team_id': {'required': False, 'type': int},
        'name': {'required': False, 'type': str},
        'table': {'required': False, 'type': str},
        'members': {'required': False, 'type': str},
        'link': {'required': False, 'type': str},
        'is_anchor': {'required': False, 'type': bool},
    }
    kwargs = clean_fields(fields, kwargs)

    teams = Team.objects.all()
    if 'team_id' in kwargs:
        teams = teams.filter(pk=kwargs['team_id'])
    if 'name' in kwargs:
        teams = teams.filter(name__icontains=kwargs['name'])
    if 'table' in kwargs:
        teams = teams.filter(table__icontains=kwargs['table'])
    if 'members' in kwargs:
        teams = teams.filter(members__icontains=kwargs['members'])
    if 'link' in kwargs:
        teams = teams.filter(link__icontains=kwargs['link'])
    if 'is_anchor' in kwargs:
        teams = teams.filter(is_anchor__exact=kwargs['is_anchor'])

    return teams


def update(team_id: int,
           name: str = None,
           table: str = None,
           members: str = None,
           link: str = None,
           is_anchor: bool = None):
    kwargs = locals()
    fields = {
        'team_id': {'required': True, 'type': int},
        'name': {'required': False, 'type': str},
        'table': {'required': False, 'type': str},
        'members': {'required': False, 'type': str},
        'link': {'required': False, 'type': str},
        'is_anchor': {'required': False, 'type': bool},
    }
    kwargs = clean_fields(fields, kwargs)

    team_id = kwargs.pop('team_id')
    Team.objects.filter(pk=team_id).update(**kwargs)
    team = Team.objects.get(pk=team_id)
    return team


def delete(team_id: int):
    kwargs = locals()
    fields = {
        'team_id': {'required': True, 'type': int},
    }
    kwargs = clean_fields(fields, kwargs)

    Team.objects.get(pk=kwargs['team_id']).delete()
