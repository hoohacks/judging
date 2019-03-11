from django.forms.models import model_to_dict
from django.shortcuts import render


from ..models import Criteria
from ..utils.api import *


def create(name: str,
           description: str = None,
           min_score: int = None,
           max_score: int = None,
           weight: float = None):
    kwargs = locals()
    fields = {
        'name': {'required': True, 'type': str},
        'description': {'required': False, 'type': str},
        'min_score': {'required': False, 'type': int},
        'max_score': {'required': False, 'type': int},
        'weight': {'required': False, 'type': float},
    }
    kwargs = clean_fields(fields, kwargs)
    criteria = Criteria.objects.create(**kwargs)
    return criteria


def search(criteria_id: int = None,
           name: str = None,
           description: str = None):
    kwargs = locals()
    fields = {
        'criteria_id': {'required': False, 'type': int},
        'name': {'required': False, 'type': str},
        'description': {'required': False, 'type': str},
    }
    kwargs = clean_fields(fields, kwargs)

    criterias = Criteria.objects.all()
    if 'criteria_id' in kwargs:
        criterias = criterias.filter(pk=kwargs['criteria_id'])
    if 'name' in kwargs:
        criterias = criterias.filter(name__iexact=kwargs['name'])
    if 'description' in kwargs:
        criterias = criterias.filter(
            description__icontains=kwargs['description'])
    return criterias


def update(criteria_id: int,
           name: str = None,
           description: str = None,
           min_score: int = None,
           max_score: int = None,
           weight: float = None):
    kwargs = locals()
    fields = {
        'criteria_id': {'required': True, 'type': int},
        'name': {'required': False, 'type': str},
        'description': {'required': False, 'type': str},
        'min_score': {'required': False, 'type': int},
        'max_score': {'required': False, 'type': int},
        'weight': {'required': False, 'type': float},
    }
    kwargs = clean_fields(fields, kwargs)

    criteria_id = kwargs.pop('criteria_id')
    Criteria.objects.filter(pk=criteria_id).update(**kwargs)
    criteria = Criteria.objects.get(pk=criteria_id)
    return criteria


def delete(criteria_id: int):
    kwargs = locals()
    fields = {
        'criteria_id': {'required': True, 'type': int},
    }
    kwargs = clean_fields(fields, kwargs)

    Criteria.objects.get(pk=kwargs['criteria_id']).delete()

