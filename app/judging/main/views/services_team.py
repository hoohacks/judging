import csv
from io import StringIO
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


@login_required
def import_teams_from_devpost(request):
    """Import teams from devpost submissions data export.

    The team names, submission URLs, and opt-in prize categories are captured.
    Unlike other POST-REDIRECT-GET-RERENDER handlers, this function will fully
    redirect to the edit teams page, causing a full refresh. The reason for this
    is handling file uploads with ajax is rather annoying.
    """
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Must be admin', extra_tags='import_teams_from_devpost')
        return redirect('import_teams_from_devpost')

    if request.method == 'GET':
        return redirect('edit_teams')
    elif request.method == 'POST':
        context = {}
        # source: https://www.pythoncircle.com/post/30/how-to-upload-and-process-the-csv-file-in-django/
        csv_file = request.FILES.get('devpost_csv', None)

        # check is a csv file
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Uploaded file must be a .csv')
            return redirect('import_teams_from_devpost')

        # check if file too large
        if csv_file.multiple_chunks():
            messages.error(request, 'Uh oh, file ({:.2f}MB) too large, max (2.5MB)'.format(
                csv_file.size / (1000 * 1000)))
            return redirect('import_teams_from_devpost')

        data = csv_file.read().decode("utf-8")
        reader = csv.reader(StringIO(data), csv.excel)
        headers = next(reader)
        num_teams_created = 0
        for row in reader:
            prize = row[0]
            project_name = row[1]
            project_url = row[2]

            # get or create team
            teams = Team.search(link=project_url)
            if len(teams) == 0:
                num_teams_created += 1
                team = Team.create(project_name, link=project_url)
            else:
                team = teams[0]

            if prize != '':
                # get or create category
                categories = Category.search(name=prize)
                if len(categories) == 0:
                    organizers = Event.get().organizers
                    category = Category.create(
                        name=prize, organization_id=organizers.id, is_opt_in=True)
                    messages.warning(request, '"{}" was created and assigned to "{}" by default'.format(
                        prize, organizers.name))
                else:
                    # TODO: more robust edge case checking
                    category = categories[0]

                # add team to category
                Category.add_team(category.id, team.id)
        messages.info(request, '{} new teams created'.format(num_teams_created), extra_tags='import_teams_from_devpost')
        return redirect('import_teams_from_devpost')
    return redirect('import_teams_from_devpost')



@login_required
def update_team(request):
    """Update team information.
    
    Update the team's table and return information about
    if it succeeded and if the new table was different
    from the old table.
    """
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

    kwargs = {
        'team_id': request.POST.get('team_id', None),
        'table': request.POST.get('table', None)
    }
    try:
        team = Team.search(team_id=kwargs['team_id'])[0]
        original_table = team.table
        team = Team.update(**kwargs)
    except Exception as e:
        response['reason'] = str(e)
        return response

    response['success'] = True
    response['updated'] = original_table != team.table
    return JsonResponse(response)



@login_required
def add_team(request):
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Must be admin', extra_tags='add_team')
        return HttpResponse('Must be admin')

    if request.method == 'GET':
        context = {
            'teams': Team.search(is_anchor=False).order_by('table', 'name')
        }
        return render(request, 'admin/edit_teams_list.html', context)
    elif request.method == 'POST':
        kwargs = {
            'name': request.POST.get('name', None),
            'table': request.POST.get('table', None),
            'is_anchor': request.POST.get('is_anchor', None),
        }
        try:
            team = Team.create(**kwargs)
        except Exception as e:
            messages.error(request, str(e), extra_tags='add_team')
            return redirect('add_team')
        return redirect('add_team')
    return redirect('add_team')


@login_required
def delete_team(request):
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Must be admin', extra_tags="delete_team")
        return HttpResponse('Must be admin')

    if request.method == 'GET':
        context = {
            'teams': Team.search(is_anchor=False).order_by('table', 'name')
        }
        return render(request, 'admin/edit_teams_list.html', context)
    elif request.method == 'POST':
        team_id = request.POST.get('team_id', None)
        try:
            Team.delete(team_id)
        except Exception as e:
            messages.error(request, str(e), extra_tags="delete_team")
            return redirect('delete_team')
        return redirect('delete_team')
    return redirect('delete_team')


def render_anchor_list(request):
    anchor_teams = Team.search(is_anchor=True).order_by('name')
    anchors = []
    for team in anchor_teams:
        team_demos = Demo.search(team_id=team.id)
        num_judges_completed = 0
        for demo in team_demos:
            if Demo.completed(demo.id):
                num_judges_completed += 1
        anchors.append({
            'name': team.name,
            'id': team.id,
            'num_judges_completed': num_judges_completed
        })
    context = {
        'anchors': anchors,
        'num_judges': len(User.search(is_judge=True))
    }
    return render(request, 'admin/anchors_list.html', context)


@login_required
def add_anchor(request):
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Must be admin', extra_tags="delete_team")
        return HttpResponse('Must be admin')

    if request.method == 'GET':
        return render_anchor_list(request)
    elif request.method == 'POST':
        add_team(request)
        return redirect('add_anchor')


@login_required
def delete_anchor(request):
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Must be admin', extra_tags="delete_team")
        return HttpResponse('Must be admin')

    if request.method == 'GET':
        return render_anchor_list(request)
    elif request.method == 'POST':
        delete_team(request)
        return redirect('delete_anchor')


@login_required
def assign_anchor_to_judges(request):
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Must be admin', extra_tags="delete_team")
        return HttpResponse('Must be admin')

    if request.method == 'GET':
        return render_anchor_list(request)
    elif request.method == 'POST':
        team_id = request.POST.get('team_id', None)
        if team_id:
            judges = User.search(is_judge=True)
            for judge in judges:
                Demo.create(judge_id=judge.id, team_id=team_id, if_not_exists=True)
        return redirect('assign_anchor_to_judges')