from django.forms.models import model_to_dict
from django.shortcuts import render


from ..models import Demo
from . import demo_score as DemoScore
from . import criteria as Criteria
from ..utils.api import *


def create(judge_id: int, team_id: int, if_not_exists: bool = True):
    kwargs = locals()
    fields = {
        'judge_id': {'required': True, 'type': int},
        'team_id': {'required': True, 'type': int},
        'if_not_exists': {'required': True, 'type': bool},
    }
    kwargs = clean_fields(fields, kwargs)
    demos = search(judge_id=judge_id, team_id=team_id)
    if_not_exists = kwargs.pop('if_not_exists')
    if len(demos) == 0 or not if_not_exists:
        demo = Demo.objects.create(**kwargs)
    else:
        demo = demos[0]
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


def exists(judge_id: int, team_id: int):
    return len(search(judge_id=judge_id, team_id=team_id)) > 0


def completed(demo_id: int):
    criteria = Criteria.search()
    for criterion in criteria:
        if len(DemoScore.search(demo_id=demo_id, criteria_id=criterion.id)) == 0:
            return False
    return True


def update(demo_id: int, judge_id: int = None, team_id: int = None, raw_score: float = None, norm_score: float = None):
    kwargs = locals()
    fields = {
        'demo_id': {'required': True, 'type': int},
        'judge_id': {'required': False, 'type': int},
        'team_id': {'required': False, 'type': int},
        'raw_score': {'required': False, 'type': float},
        'norm_score': {'required': False, 'type': float},
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
