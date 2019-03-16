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


@login_required
def update_organization(request):
    response = {
        'success': False,
        'updated': False,
        'reason': '',
    }
    if not (request.user.is_staff or request.user.is_superuser):
        response['reason'] = 'Must be admin'
        return JsonResponse(response)

    if request.method == 'POST':
        org_id = request.POST.get('org_id', None)
        org_name = request.POST.get('org_name', None)

        if org_id == None or org_name == None:
            response['reason'] = 'Must provide organization ID and name'
            return JsonResponse(response)

        org_name = org_name.strip()
        if org_name == '':
            response['reason'] = 'Must provide organization name'
            return JsonResponse(response)

        orgs = Organization.search(organization_id=org_id)
        if len(orgs) == 0:
            response['reason'] = 'Organization with ID {} not found'.format(
                org_id)
            return JsonResponse(response)

        original_name = orgs[0].name
        org = Organization.update(org_id, org_name)
        response['success'] = True
        response['updated'] = original_name != org.name
        response['reason'] = '"{}" changed to "{}"'.format(
            original_name, org.name)
        return JsonResponse(response)
    return JsonResponse(response)


@login_required
def add_organization(request):
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Must be admin', extra_tags='add_organization')
        return HttpResponse('Must be admin')

    if request.method == 'GET':
        context = {
            'organizations': Organization.search().order_by('name'),
            'organizers_id': Event.get().id,
        }
        return render(request, 'admin/edit_organizations_list.html', context)
    elif request.method == 'POST':
        org_name = request.POST.get('org_name', None)
        if org_name == None:
            messages.error(request, 'Must provide organization name', extra_tags='add_organization')
            return redirect('add_organization')

        org_name = org_name.strip()
        if org_name == '':
            messages.error(request, 'Must provide organization name', extra_tags='add_organization')
            return redirect('add_organization')

        orgs = Organization.search(name=org_name)
        if len(orgs) > 0:
            messages.error(request, 'Organization with same name already exists', extra_tags='add_organization')
            return redirect('add_organization')

        org = Organization.create(org_name)
        messages.info(request, 'New organization called {} created'.format(org.name), extra_tags='add_organization')
        return redirect('add_organization')
    return redirect('add_organization')


@login_required
def delete_organization(request):
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Must be admin', extra_tags="delete_organization")
        return HttpResponse('Must be admin')

    if request.method == 'GET':
        context = {
            'organizations': Organization.search().order_by('name'),
            'organizers_id': Event.get().id,
        }
        return render(request, 'admin/edit_organizations_list.html', context)
    elif request.method == 'POST':
        org_id = request.POST.get('org_id', None)
        if org_id == None:
            messages.error(request, 'Must provide organization ID', extra_tags="delete_organization")
            return redirect('delete_organization')

        orgs = Organization.search(organization_id=org_id)
        if len(orgs) == 0:
            messages.error(request, 'Organization with ID {} not found'.format(org_id), extra_tags="delete_organization")
            return redirect('delete_organization')

        Organization.delete(org_id)
        return redirect('delete_organization')
    return redirect('delete_organization')
