from itertools import product
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
def generate_judges(request):
    """DEVELOPMENT ONLY"""
    if not (request.user.is_staff or request.user.is_superuser):
        return JsonResponse({'success': False})

    if request.method == 'POST':
        first_names = ['Alice', 'Bob', 'Charlie', 'Dave', 'Eliza',
                       'Frank', 'George', 'Helena', 'Isabelle', 'John']
        last_names = ['Schuyler', 'Washington', 'Hamilton',
                      'Adams', 'Madison', 'Franklin', 'Jefferson', 'Mulligan']

        # Generate notional number of judges per organization
        orgs = Organization.search()
        organizers_id = Event.get().organizers.id
        avg_num_judges_per_org = 3
        judge_needs = []  # list of org ids, one for each judge needed
        for org in orgs:
            if org.id == organizers_id:
                continue
            for i in range(int(random.expovariate(1 / (avg_num_judges_per_org - 1))) + 1):
                judge_needs.append(org.id)

        # Create judges
        j_cnt = 0
        for fn, ln in product(first_names, last_names):
            org_id = judge_needs[j_cnt]
            username = fn[0].lower() + ln.lower()
            User.create(first_name=fn, last_name=ln, username=username,
                        password='thisismypassword', organization_id=org_id)
            j_cnt += 1
            if j_cnt >= len(judge_needs):
                break
        
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})




@login_required
def delete_all_demos(request):
    """DEVELOPMENT ONLY"""
    if not (request.user.is_staff or request.user.is_superuser):
        return JsonResponse({'success': False})

    if request.method == 'POST':
        demos = Demo.search()
        for demo in demos:
            Demo.delete(demo_id=demo.id)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
