from math import sqrt
from queue import PriorityQueue

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
def normalize_scores(request):
    response = {
        'success': False,
        'reason': ''
    }

    if request.method == 'POST':
        ### Calculate judge standard deviation offsets
        anchor_teams = Team.search(is_anchor=True)
        if len(anchor_teams) == 0:
            response['reason'] = 'No anchor teams to normalize on'
            return JsonResponse(response)

        judges = User.search(is_judge=True)

        # Compute means and standard deviations
        anchor_means = {}
        anchor_sds = {}
        all_anchor_mean = 0
        anchor_sd_mean = 0
        for team in anchor_teams:
            team_scores = [demo.raw_score for demo in Demo.search(team_id=team.id)]
            scores_mean = sum(team_scores) / len(team_scores)
            scores_var = sum([pow(score - scores_mean, 2) for score in team_scores]) / len(team_scores)
            scores_sd = sqrt(scores_var)
            anchor_means[team.id] = scores_mean
            anchor_sds[team.id] = scores_sd


        # Compute judge sd offsets
        for judge in judges:
            offsets = []
            for team in anchor_teams:
                demos = Demo.search(judge_id=judge.id, team_id=team.id)
                if len(demos) != 0:
                    offsets.append((demos[0].raw_score - anchor_means[team.id]))
                    # Could also divide this by anchor_sds[team.id] to get the zscore
                    # For simplicity, let's assume the distribution of scores doesn't change
                    #   for each team, an arguably-reasonable assumption
            if len(offsets) > 0:
                User.update(user_id=judge.id, sd_offset=sum(offsets) / len(offsets))

        # Compute demo norm_scores
        for demo in Demo.search():
            if demo.team.is_anchor:
                continue
            Demo.update(demo_id=demo.id, norm_score=demo.raw_score-demo.judge.sd_offset)

        response['success'] = True
        return JsonResponse(response)
    return JsonResponse(response)


@login_required
def assign_demos(request):
    """Assign demos to judges.

    Only staff can assign demos.
    """
    if not (request.user.is_staff or request.user.is_superuser):
        return JsonResponse({'success': False, 'reason': 'Must be admin'})

    if request.method != 'GET':
        return JsonResponse({'success': False, 'reason': 'Must be GET'})

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
            judges_for_category = category.judges.all()
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
