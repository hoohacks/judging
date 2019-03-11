from django.forms.models import model_to_dict
from django.shortcuts import render


from ..models import Criteria, CriteriaLabel
from ..utils.api import *


def create(criteria_id: int, score: int, label: str):
    kwargs = locals()
    fields = {
        'criteria_id': {'required': True, 'type': int},
        'score': {'required': True, 'type': int},
        'label': {'required': True, 'type': str},
    }
    kwargs = clean_fields(fields, kwargs)
    criteria_label = CriteriaLabel.objects.create(**kwargs)
    return criteria_label


def search(criteria_label_id: int = None,
                          criteria_id: int = None,
                          score: int = None,
                          label: str = None):
    kwargs = locals()
    fields = {
        'criteria_label_id': {'required': False, 'type': int},
        'criteria_id': {'required': False, 'type': int},
        'score': {'required': False, 'type': int},
        'label': {'required': False, 'type': str},
    }
    kwargs = clean_fields(fields, kwargs)

    criteria_labels = CriteriaLabel.objects.all()
    if 'criteria_label_id' in kwargs:
        criteria_labels = criteria_labels.filter(
            pk=kwargs['criteria_label_id'])
    if 'criteria_id' in kwargs:
        criteria_labels = criteria_labels.filter(
            criteria__id__exact=kwargs['criteria_id'])
    if 'score' in kwargs:
        criteria_labels = criteria_labels.filter(score__exact=kwargs['score'])
    if 'label' in kwargs:
        criteria_labels = criteria_labels.filter(
            label__icontains=kwargs['label'])

    return criteria_labels


def update(criteria_label_id: int,
                          criteria_id: int = None,
                          score: int = None,
                          label: str = None):
    kwargs = locals()
    fields = {
        'criteria_label_id': {'required': True, 'type': int},
        'criteria_id': {'required': False, 'type': int},
        'score': {'required': False, 'type': int},
        'label': {'required': False, 'type': str},
    }
    kwargs = clean_fields(fields, kwargs)

    criteria_label_id = kwargs.pop('criteria_label_id')
    if 'criteria_id' in kwargs:
        criteria_id = kwargs.pop('criteria_id')
        criteria = Criteria.objects.get(pk=criteria_id)
        kwargs['criteria'] = criteria
    CriteriaLabel.objects.filter(pk=criteria_label_id).update(**kwargs)
    criteria_label = CriteriaLabel.objects.get(pk=criteria_label_id)
    return criteria_label


def delete(criteria_label_id: int):
    kwargs = locals()
    fields = {
        'criteria_label_id': {'required': True, 'type': int},
    }
    kwargs = clean_fields(fields, kwargs)

    CriteriaLabel.objects.get(pk=kwargs['criteria_label_id']).delete()
