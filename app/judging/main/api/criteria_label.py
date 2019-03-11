from django.forms.models import model_to_dict
from django.shortcuts import render


from ..models import Criteria, CriteriaLabel
from ..utils.api import *

# criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE)
# score = models.IntegerField()
# label = models.CharField(max_length=255)


def criteria_label_create(request):
    check_method(request, 'POST')
    fields = {
        'criteria_id': {'required': True, 'type': int},
        'score': {'required': True, 'type': int},
        'label': {'required': True, 'type': str},
    }
    kwargs = extract_fields(fields, request.POST)
    criteria_label = CriteriaLabel.objects.create(**kwargs)
    return JsonResponse(model_to_dict(criteria_label))


def criteria_label_search(request):
    check_method(request, 'GET')
    fields = {
        'criteria_label_id': {'required': False, 'type': int},
        'criteria_id': {'required': False, 'type': int},
        'score': {'required': False, 'type': int},
        'label': {'required': False, 'type': str},
    }
    kwargs = extract_fields(fields, request.GET)

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

    results = {
        'results': [model_to_dict(criteria_label) for criteria_label in criteria_labels]
    }
    return JsonResponse(results)


def criteria_label_update(request):
    check_method(request, 'POST')
    fields = {
        'criteria_label_id': {'required': True, 'type': int},
        'criteria_id': {'required': False, 'type': int},
        'score': {'required': False, 'type': int},
        'label': {'required': False, 'type': str},
    }
    kwargs = extract_fields(fields, request.POST)

    criteria_label_id = kwargs.pop('criteria_label_id')
    if 'criteria_id' in kwargs:
        criteria_id = kwargs.pop('criteria_id')
        criteria = Criteria.objects.get(pk=criteria_id)
        kwargs['criteria'] = criteria
    CriteriaLabel.objects.filter(pk=criteria_label_id).update(**kwargs)
    criteria_label = CriteriaLabel.objects.get(pk=criteria_label_id)
    return JsonResponse(model_to_dict(criteria_label))


def criteria_label_delete(request):
    check_method(request, 'POST')
    fields = {
        'criteria_label_id': {'required': True, 'type': int},
    }
    kwargs = extract_fields(fields, request.POST)

    CriteriaLabel.objects.get(pk=kwargs['criteria_label_id']).delete()
    return JsonResponse({})
