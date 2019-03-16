from django.forms.models import model_to_dict
from django.shortcuts import render


from ..models import DemoScore
from ..api import criteria as Criteria
from ..api import demo as Demo
from ..utils.api import *


def create(demo_id: int, criteria_id: int, value: int):
    """Create OR UPDATE demo score."""
    kwargs = locals()
    fields = {
        'demo_id': {'required': True, 'type': int},
        'criteria_id': {'required': True, 'type': int},
        'value': {'required': True, 'type': int},
    }
    kwargs = clean_fields(fields, kwargs)
    if exists(demo_id=kwargs['demo_id'], criteria_id=kwargs['criteria_id']):
        demo_score = search(demo_id=kwargs['demo_id'], criteria_id=kwargs['criteria_id'])
    else:
        demo_score = DemoScore.objects.create(**kwargs)

    # Recompute demo's total score
    new_score = 0
    related_demo_scores = search(demo_id=demo_id)
    for demo_score in related_demo_scores:
        new_score += demo_score.value * demo_score.criteria.weight
    Demo.update(demo_id=demo_id, raw_score=new_score)
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


def exists(demo_id: int, criteria_id: int):
    return len(search(demo_id=demo_id, criteria_id=criteria_id)) > 0


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

    # Recompute demo's total score
    new_score = 0
    related_demo_scores = search(demo_id=demo_id)
    for demo_score in related_demo_scores:
        new_score += demo_score.value * demo_score.criteria.weight
    Demo.update(demo_id=demo_id, raw_score=new_score)

    return demo_score


def delete(demo_score_id: int):
    kwargs = locals()
    fields = {
        'demo_score_id': {'required': True, 'type': int},
    }
    kwargs = clean_fields(fields, kwargs)

    demo_score = DemoScore.objects.get(pk=kwargs['demo_score_id'])
    demo = demo_score.demo  # save before deleting demo score
    demo_score.delete()

    # Recompute demo's total score
    new_score = 0
    related_demo_scores = search(demo_id=demo.id)
    for demo_score in related_demo_scores:
        new_score += demo_score.value * demo_score.criteria.weight
    Demo.update(demo_id=demo.id, raw_score=new_score)
