from queue import PriorityQueue
import random

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


@login_required
def simulate_demos(request):
    """DEVELOPMENT ONLY"""
    if not (request.user.is_staff or request.user.is_superuser):
        return JsonResponse({'success': False})

    if request.method == 'POST':
        judge_distributions = {}
        team_distributions = {}
        for demo in Demo.search():
            if Demo.completed(demo.id):
                continue
            if demo.judge.id not in judge_distributions:
                judge_distributions[demo.judge.id] = {
                    'mean': random.gauss(0, 0.25),
                    'std': random.gauss(0.1, 0.1)
                }
            if demo.team.id not in team_distributions:
                team_distributions[demo.team.id] = {
                    'mean': random.gauss(3, 0.5),
                    'std': random.gauss(0.5, 0.1)
                }
            for criteria in Criteria.search():
                team_score = random.gauss(
                    team_distributions[demo.team.id]['mean'], team_distributions[demo.team.id]['std'])
                judge_adjust = random.gauss(
                    judge_distributions[demo.judge.id]['mean'], judge_distributions[demo.judge.id]['std'])
                demo_score = round(team_score + judge_adjust)
                demo_score = min(max(demo_score, 1), 5)
                DemoScore.create(demo.id, criteria.id, demo_score)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
def assign_demos(request):
    """Assign demos to judges.

    Only staff can assign demos.
    """
    if not (request.user.is_staff or request.user.is_superuser):
        return JsonResponse({'success': False, 'reason': 'Must be admin'})

    if request.method != 'POST':
        return JsonResponse({'success': False, 'reason': 'Must be POST'})


    teams = Team.search()
    judges = User.search(is_judge=True)

    # ensure everyone is signed up for non-opt-in prizes
    non_opt_in_categories = Category.search(is_opt_in=False)
    for team in teams:
        for category in non_opt_in_categories:
            Category.add_team(category.id, team.id)

    # first, assign teams to sponsor prizes
    # TODO: currently does not guarantee min_judges
    organizers = Event.get().organizers
    for category in Category.search():
        if category.organization.id == organizers.id:  # skip organizer categories
            continue
        for team in category.submissions.all():
            judges_for_category = User.search(
                is_judge=True, organization_id=category.organization.id)
            for judge in judges_for_category:
                Demo.create(judge.id, team.id, if_not_exists=True)

    # second, assign teams to non-sponsor prizes
    # priority queue for teams (priority = number of demos already assigned)
    # priority queue for judges (priority = number of demos already assigned)
    demos_left = {}
    team_q = PriorityQueue()
    for team in teams:
        demos = Demo.search(team_id=team.id)
        priority = len(demos)

        for category in Category.search():
            if category.organization.id == organizers.id:
                if team.id not in demos_left:
                    demos_left[team.id] = {}
                demos_left[team.id][category.id] = category.min_judges
        team_q.put((priority, team.id))

    judge_q = PriorityQueue()
    for judge in judges:
        demos = Demo.search(judge_id=judge.id)
        priority = len(demos)
        judge_q.put((priority, judge.id))

    while not team_q.empty():
        team_priority, team_id = team_q.get()

        if not any(demos_left[team_id].values()):  # if no more demos needed
            continue

        for category_id, num_needed in demos_left[team_id].items():
            if num_needed == 0:
                continue
            team_priority += 1
            demos_left[team_id][category_id] -= 1
            judge_priority, judge_id = judge_q.get()
            judge_priority += 1
            judge_q.put((judge_priority, judge_id))
            Demo.create(judge_id, team_id, if_not_exists=True)
            break

        team_q.put((team_priority, team_id))

    return JsonResponse({'success': True})
