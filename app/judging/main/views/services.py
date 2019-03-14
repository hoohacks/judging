from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


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
    response = {
        'success': False,
        'reason': ''
    }
    if not (request.user.is_staff or request.user.is_superuser):
        response['reason'] = 'Must be admin'
        return JsonResponse(response)

    if request.method == 'POST':
        org_name = request.POST.get('org_name', None)
        if org_name == None:
            response['reason'] = 'Must provide organization name'
            return JsonResponse(response)

        org_name = org_name.strip()
        if org_name == '':
            response['reason'] = 'Must provide organization name'
            return JsonResponse(response)

        orgs = Organization.search(name=org_name)
        if len(orgs) > 0:
            response['reason'] = 'Organization with same name already exists'
            return JsonResponse(response)

        org = Organization.create(org_name)
        response['success'] = True
        response['org'] = {
            'id': org.id,
            'name': org.name
        }
        response['reason'] = 'New organization called {} created'.format(
            org.name)
        return JsonResponse(response)
    return JsonResponse(response)


@login_required
def delete_organization(request):
    response = {
        'success': False,
        'reason': ''
    }
    if not (request.user.is_staff or request.user.is_superuser):
        response['reason'] = 'Must be admin'
        return JsonResponse(response)

    if request.method == 'POST':
        org_id = request.POST.get('org_id', None)
        if org_id == None:
            response['reason'] = 'Must provide organization ID'
            return JsonResponse(response)

        orgs = Organization.search(organization_id=org_id)
        if len(orgs) == 0:
            response['reason'] = 'Organization with ID {} not found'.format(
                org_id)
            return JsonResponse(response)

        Organization.delete(org_id)
        response['success'] = True
        return JsonResponse(response)
    return JsonResponse(response)



@login_required
def get_scores(request):
    response = {
        'success': False,
        'reason': ''
    }

    if request.method == 'POST':
        team_id = request.POST.get('team', None)
        if team_id == None:
            response['reason'] = 'Must provide team ID'
            return JsonResponse(response)

        teams = Team.search(team_id=team_id)
        if len(teams) == 0:
            response['reason'] = 'Team with ID {} not found'.format(
                team_id)
            return JsonResponse(response)

        demos = Demo.search(judge_id=request.user.id, team_id=team_id)
        if len(demos) == 0:
            response['reason'] = 'Demo not found'
            return JsonResponse(response)
        demo = demos[0]

        demo_scores = DemoScore.search(demo_id=demo.id)
        demo_scores_dict = {}
        for score in demo_scores:
            demo_scores_dict[score.criteria.id] = score.value
        response['success'] = True
        response['data'] = demo_scores_dict
        return JsonResponse(response)
    return JsonResponse(response)
