from django.forms.models import model_to_dict
from django.shortcuts import render


from ..models import Event
from ..utils.api import *


def event_create(request):
    check_method(request, 'POST')
    fields = {
        'name': {'required': True, 'type': str},
    }
    kwargs = extract_fields(fields, request.POST)
    event = Event.objects.create(**kwargs)
    return JsonResponse(model_to_dict(event))


def event_search(request):
    check_method(request, 'GET')
    fields = {
        'event_id': {'required': False, 'type': int},
        'name': {'required': False, 'type': str},
    }
    kwargs = extract_fields(fields, request.GET)

    events = Event.objects.all()
    if 'event_id' in kwargs:
        events = events.filter(pk=kwargs['event_id'])
    if 'name' in kwargs:
        events = events.filter(name__iexact=kwargs['name'])

    results = {
        'results': [model_to_dict(event) for event in events]
    }
    return JsonResponse(results)


def event_update(request):
    check_method(request, 'POST')
    fields = {
        'event_id': {'required': True, 'type': int},
        'name': {'required': False, 'type': str},
    }
    kwargs = extract_fields(fields, request.POST)

    event_id = kwargs.pop('event_id')
    Event.objects.filter(pk=event_id).update(**kwargs)
    event = Event.objects.get(pk=event_id)
    return JsonResponse(model_to_dict(event))


def event_delete(request):
    check_method(request, 'POST')
    fields = {
        'event_id': {'required': True, 'type': int},
    }
    kwargs = extract_fields(fields, request.POST)

    Event.objects.get(pk=kwargs['event_id']).delete()
    return JsonResponse({})
