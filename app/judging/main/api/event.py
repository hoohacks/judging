from django.forms.models import model_to_dict
from django.shortcuts import render


from ..models import Event
from ..utils.api import *


def create(name: str, organizers_id: int = None):
    kwargs = locals()
    fields = {
        'name': {'required': True, 'type': str},
        'organizers_id': {'required': False, 'type': int},
    }
    kwargs = clean_fields(fields, kwargs)
    event = Event.objects.create(**kwargs)
    return event


def search(event_id: int = None, name: str = None, organizers_id: int = None):
    kwargs = locals()
    fields = {
        'event_id': {'required': False, 'type': int},
        'name': {'required': False, 'type': str},
        'organizers_id': {'required': False, 'type': int},
    }
    kwargs = clean_fields(fields, kwargs)

    events = Event.objects.all()
    if 'event_id' in kwargs:
        events = events.filter(pk=kwargs['event_id'])
    if 'name' in kwargs:
        events = events.filter(name__iexact=kwargs['name'])
    return events.order_by('-event_id')


def get():
    """Get event that was last created"""
    return Event.objects.all().order_by('-id').first()


def update(event_id: int, name: str = None, organizers_id: int = None):
    kwargs = locals()
    fields = {
        'event_id': {'required': True, 'type': int},
        'name': {'required': False, 'type': str},
        'organizers_id': {'required': False, 'type': int},
    }
    kwargs = clean_fields(fields, kwargs)

    event_id = kwargs.pop('event_id')
    Event.objects.filter(pk=event_id).update(**kwargs)
    event = Event.objects.get(pk=event_id)
    return event


def delete(event_id: int):
    kwargs = locals()
    fields = {
        'event_id': {'required': True, 'type': int},
    }
    kwargs = clean_fields(fields, kwargs)

    Event.objects.get(pk=kwargs['event_id']).delete()
