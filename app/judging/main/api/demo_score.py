from django.forms.models import model_to_dict
from django.shortcuts import render


from ..models import DemoScore, Team, User
from ..utils.api import *


def create(demo_id: int, criteria_id: int, value: int):
    kwargs = locals()
    fields = {
        'demo_id': {'required': True, 'type': int},
        'criteria_id': {'required': True, 'type': int},
        'value': {'required': True, 'type': int},
    }
    kwargs = clean_fields(fields, kwargs)
    demo_score = DemoScore.objects.create(**kwargs)
    return demo_score


def search(demo_score_id: int = None,
           demo_id: int = None,
           criteria_id: int = None,
           value: int = None):
    kwargs = locals()
    fields = {
        'demo_score_id': {'required': False, 'type': int},
        'demo_id': {'required': False, 'type': int},
        'criteria_id': {'required': False, 'type': int},
        'value': {'required': False, 'type': int},
    }
    kwargs = clean_fields(fields, kwargs)

    demo_scores = DemoScore.objects.all()
    if 'demo_score_id' in kwargs:
        demo_scores = demo_scores.filter(pk=kwargs['demo_score_id'])
    if 'demo_id' in kwargs:
        demo_scores = demo_scores.filter(demo__id__exact=kwargs['demo_id'])
    if 'criteria_id' in kwargs:
        demo_scores = demo_scores.filter(
            criteria__id__exact=kwargs['criteria_id'])
    if 'value' in kwargs:
        demo_scores = demo_scores.filter(value__exact=kwargs['value'])
    return demo_scores


def update(demo_score_id: int,
           demo_id: int = None,
           criteria_id: int = None,
           value: int = None):
    kwargs = locals()
    fields = {
        'demo_score_id': {'required': True, 'type': int},
        'demo_id': {'required': False, 'type': int},
        'criteria_id': {'required': False, 'type': int},
        'value': {'required': False, 'type': int},
    }
    kwargs = clean_fields(fields, kwargs)

    demo_score_id = kwargs.pop('demo_score_id')
    DemoScore.objects.filter(pk=demo_score_id).update(**kwargs)
    demo_score = DemoScore.objects.get(pk=demo_score_id)
    return demo_score


def delete(demo_score_id: int):
    kwargs = locals()
    fields = {
        'demo_score_id': {'required': True, 'type': int},
    }
    kwargs = clean_fields(fields, kwargs)

    DemoScore.objects.get(pk=kwargs['demo_score_id']).delete()
