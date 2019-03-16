import re

from bs4 import BeautifulSoup
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import requests


from ..api import user as User
from ..api import organization as Organization
from ..api import event as Event
from ..api import team as Team
from ..api import category as Category
from ..api import criteria as Criteria
from ..api import criteria_label as CriteriaLabel
from ..api import demo as Demo
from ..api import demo_score as DemoScore
from ..utils.api import extract_fields, ApiException


@login_required
def import_categories_from_devpost(request):
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Must be admin', extra_tags='import_categories_from_devpost')
        return redirect('import_categories_from_devpost')

    if request.method == 'GET':
        context = {
            'categories': Category.search().order_by('name')
        }
        return render(request, 'admin/edit_categories_list.html', context)
    elif request.method == 'POST':
        # Extract devpost url from request data
        fields = {'devpost_url': {'required': True, 'type': str}}
        try:
            kwargs = extract_fields(fields, request.POST)
        except ApiException as e:
            messages.error(request, str(e), extra_tags='import_categories_from_devpost')
            return redirect('import_categories_from_devpost')

        # Get devpost data
        devpost_url = kwargs.pop('devpost_url')
        r = requests.get(devpost_url)
        if r.status_code != 200:
            messages.error(request, 'Bad URL, Response <{}>'.format(r.status_code), extra_tags='import_categories_from_devpost')
            return redirect('import_categories_from_devpost')
        soup = BeautifulSoup(r.text, 'html.parser')

        # Scrape prize information
        prize_list_items = soup.find_all('li', attrs={'class': 'prize'})
        raw_prize_texts = []
        for prize_li in prize_list_items:
            raw_prize_texts.append(prize_li.find('h6').text.strip())

        # Extract name and number of winners
        # Example: "Best Overall Hack   (2)"
        pattern = re.compile('\(\d+\)$')
        prizes = []
        for raw_text in raw_prize_texts:
            pattern_match = pattern.search(raw_text)
            if pattern_match:
                start_index = pattern_match.span()[0]
                prizes.append({
                    'name': raw_text[:start_index].strip(),
                    'num_winners': int(pattern_match.group()[1:-1])
                })
            else:
                prizes.append({
                    'name': raw_text,
                    'num_winners': 1
                })

        # Actually create prizes if they don't exist
        created_categories = []
        for prize in prizes:
            if len(Category.search(name=prize['name'])) > 0:
                continue

            organizers_id = Event.get().organizers.id
            Category.create(name=prize['name'],
                            organization_id=organizers_id,
                            number_winners=prize['num_winners'])
        return redirect('import_categories_from_devpost')
    return redirect('import_categories_from_devpost')



@login_required
def update_category(request):
    response = {
        'success': False,
        'updated': False,
        'reason': '',
    }
    if not (request.user.is_staff or request.user.is_superuser):
        response['reason'] = 'Must be admin'
        return JsonResponse(response)

    if request.method != 'POST':
        response['reason'] = 'Must be POST request'
        return JsonResponse(response)

    # Extract devpost url from request data
    kwargs = {
        'category_id': request.POST.get('category_id', None),
        'name': request.POST.get('name', None),
        'organization_id': request.POST.get('organization', None),
        'is_opt_in': request.POST.get('is_opt_in', None),
        'number_winners': request.POST.get('number_winners', None),
        'min_judges': request.POST.get('min_judges', None),
    }
    try:
        category = Category.update(**kwargs)
    except ApiException as e:
        response['reason'] = str(e)
        return response

    response['success'] = True
    response['updated'] = True  # TODO: check if anything actually changed
    return JsonResponse(response)



@login_required
def add_category(request):
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Must be admin', extra_tags='add_category')
        return HttpResponse('Must be admin')

    if request.method == 'GET':
        context = {
            'categories': Category.search().order_by('name'),
            'organizations': Organization.search().order_by('name'),
            'organizers_id': Event.get().id,
        }
        return render(request, 'admin/edit_categories_list.html', context)
    elif request.method == 'POST':
        kwargs = {
            'name': request.POST.get('name', None),
            'organization_id': request.POST.get('organization', None),
            'is_opt_in': request.POST.get('is_opt_in', None),
            'number_winners': request.POST.get('number_winners', None),
            'min_judges': request.POST.get('min_judges', None)
        }
        try:
            category = Category.create(**kwargs)
        except Exception as e:
            messages.error(request, str(e), extra_tags='add_category')
            return redirect('add_category')  # these three return statements are dumb
        return redirect('add_category')  # because they could all be collapsed into one
    return redirect('add_category')  # but I'm going to keep it this way


@login_required
def delete_category(request):
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Must be admin', extra_tags="delete_category")
        return HttpResponse('Must be admin')

    if request.method == 'GET':
        context = {
            'categories': Category.search().order_by('name'),
            'organizations': Organization.search().order_by('name'),
            'organizers_id': Event.get().id,
        }
        return render(request, 'admin/edit_categories_list.html', context)
    elif request.method == 'POST':
        category_id = request.POST.get('category_id', None)
        try:
            Category.delete(category_id)
        except Exception as e:
            messages.error(request, str(e), extra_tags="delete_category")
            return redirect('delete_category')  # sigh
        return redirect('delete_category')  # ...
    return redirect('delete_category')  # see above
