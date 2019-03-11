from django.forms.models import model_to_dict
from django.shortcuts import render


from ..models import Demo, Team, User
from ..utils.api import *


def create(judge_id: int, team_id: int):
    kwargs = locals()
    fields = {
        'judge_id': {'required': True, 'type': int},
        'team_id': {'required': True, 'type': int},
    }
    kwargs = clean_fields(fields, kwargs)
    demo = Demo.objects.create(**kwargs)
    return demo


def search(demo_id: int = None, judge_id: int = None, team_id: int = None):
    kwargs = locals()
    fields = {
        'demo_id': {'required': False, 'type': int},
        'judge_id': {'required': False, 'type': int},
        'team_id': {'required': False, 'type': int},
    }
    kwargs = clean_fields(fields, kwargs)

    demos = Demo.objects.all()
    if 'demo_id' in kwargs:
        demos = demos.filter(pk=kwargs['demo_id'])
    if 'judge_id' in kwargs:
        demos = demos.filter(judge__id__exact=kwargs['judge_id'])
    if 'team_id' in kwargs:
        demos = demos.filter(team__id__exact=kwargs['team_id'])
    return demos


def update(demo_id: int, judge_id: int = None, team_id: int = None):
    kwargs = locals()
    fields = {
        'demo_id': {'required': True, 'type': int},
        'judge_id': {'required': False, 'type': int},
        'team_id': {'required': False, 'type': int},
    }
    kwargs = clean_fields(fields, kwargs)

    demo_id = kwargs.pop('demo_id')
    Demo.objects.filter(pk=demo_id).update(**kwargs)
    demo = Demo.objects.get(pk=demo_id)
    return demo


def delete(demo_id: int):
    kwargs = locals()
    fields = {
        'demo_id': {'required': True, 'type': int},
    }
    kwargs = clean_fields(fields, kwargs)

    Demo.objects.get(pk=kwargs['demo_id']).delete()

