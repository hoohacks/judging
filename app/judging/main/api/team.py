from django.forms.models import model_to_dict
from django.shortcuts import render


from ..models import Team
from ..utils.api import *


def team_create(request):
    check_method(request, 'POST')
    fields = {
        'name': {'required': True, 'type': str},
        'table': {'required': False, 'type': str},
        'members': {'required': False, 'type': str},
        'link': {'required': True, 'type': str},
        'is_anchor': {'required': False, 'type': bool},
    }
    kwargs = extract_fields(fields, request.POST)
    team = Team.objects.create(**kwargs)
    return JsonResponse(model_to_dict(team))


def team_search(request):
    check_method(request, 'GET')
    fields = {
        'team_id': {'required': False, 'type': int},
        'name': {'required': False, 'type': str},
        'table': {'required': False, 'type': str},
        'members': {'required': False, 'type': str},
        'link': {'required': False, 'type': str},
        'is_anchor': {'required': False, 'type': bool},
    }
    kwargs = extract_fields(fields, request.GET)

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

    results = {
        'results': [model_to_dict(team) for team in teams]
    }
    return JsonResponse(results)


def team_update(request):
    check_method(request, 'POST')
    fields = {
        'team_id': {'required': True, 'type': int},
        'name': {'required': False, 'type': str},
        'table': {'required': False, 'type': str},
        'members': {'required': False, 'type': str},
        'link': {'required': False, 'type': str},
        'is_anchor': {'required': False, 'type': bool},
    }
    kwargs = extract_fields(fields, request.POST)

    team_id = kwargs.pop('team_id')
    Team.objects.filter(pk=team_id).update(**kwargs)
    team = Team.objects.get(pk=team_id)
    return JsonResponse(model_to_dict(team))


def team_delete(request):
    check_method(request, 'POST')
    fields = {
        'team_id': {'required': True, 'type': int},
    }
    kwargs = extract_fields(fields, request.POST)

    Team.objects.get(pk=kwargs['team_id']).delete()
    return JsonResponse({})
