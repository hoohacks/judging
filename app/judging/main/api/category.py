from django.forms.models import model_to_dict
from django.shortcuts import render


from ..models import Category, Team
from ..utils.api import *


def serialize_category(category):
    obj = model_to_dict(category, fields=[
                        'id', 'name', 'description', 'organization_id', 'number_winners'])
    obj['submissions'] = [model_to_dict(sub)
                          for sub in category.submissions.all()]
    return obj


def category_create(request):
    check_method(request, 'POST')
    fields = {
        'name': {'required': True, 'type': str},
        'description': {'required': False, 'type': str},
        'organization_id': {'required': True, 'type': int},
        'number_winners': {'required': False, 'type': int},
    }
    kwargs = extract_fields(fields, request.POST)
    category = Category.objects.create(**kwargs)
    return JsonResponse(serialize_category(category))


def category_search(request):
    check_method(request, 'GET')
    fields = {
        'category_id': {'required': False, 'type': int},
        'name': {'required': False, 'type': str},
        'description': {'required': False, 'type': str},
        'organization_id': {'required': False, 'type': int},
        'number_winners': {'required': False, 'type': int},
    }
    kwargs = extract_fields(fields, request.GET)

    categories = Category.objects.all()
    if 'category_id' in kwargs:
        categories = categories.filter(pk=kwargs['category_id'])
    if 'name' in kwargs:
        categories = categories.filter(name__icontains=kwargs['name'])
    if 'description' in kwargs:
        categories = categories.filter(
            description__icontains=kwargs['description'])
    if 'organization_id' in kwargs:
        categories = categories.filter(
            organization__id__exact=kwargs['organization_id'])
    if 'number_winners' in kwargs:
        categories = categories.filter(
            number_winners__exact=kwargs['number_winners'])

    results = {
        'results': [serialize_category(category) for category in categories]
    }
    return JsonResponse(results)


def category_update(request):
    check_method(request, 'POST')
    fields = {
        'category_id': {'required': True, 'type': int},
        'name': {'required': False, 'type': str},
        'description': {'required': False, 'type': str},
        'organization_id': {'required': False, 'type': int},
        'number_winners': {'required': False, 'type': int},
    }
    kwargs = extract_fields(fields, request.POST)

    category_id = kwargs.pop('category_id')
    Category.objects.filter(pk=category_id).update(**kwargs)
    category = Category.objects.get(pk=category_id)
    return JsonResponse(serialize_category(category))


def category_delete(request):
    check_method(request, 'POST')
    fields = {
        'category_id': {'required': True, 'type': int},
    }
    kwargs = extract_fields(fields, request.POST)

    Category.objects.get(pk=kwargs['category_id']).delete()
    return JsonResponse({})


def category_add_team(request):
    check_method(request, 'POST')
    fields = {
        'category_id': {'required': True, 'type': int},
        'team_id': {'required': True, 'type': int},
    }
    kwargs = extract_fields(fields, request.POST)

    category = Category.objects.get(pk=kwargs['category_id'])
    team = Team.objects.get(pk=kwargs['team_id'])
    category.submissions.add(team)

    return JsonResponse(serialize_category(category))


def category_remove_team(request):
    check_method(request, 'POST')
    fields = {
        'category_id': {'required': True, 'type': int},
        'team_id': {'required': True, 'type': int},
    }
    kwargs = extract_fields(fields, request.POST)

    category = Category.objects.get(pk=kwargs['category_id'])
    team = Team.objects.get(pk=kwargs['team_id'])
    category.submissions.remove(team)

    return JsonResponse(serialize_category(category))
