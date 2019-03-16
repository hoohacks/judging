from collections import deque

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


from ..api import user as User
from ..api import organization as Organization
from ..api import event as Event
from ..api import team as Team
from ..api import category as Category
from ..api import criteria as Criteria
from ..api import criteria_label as CriteriaLabel
from ..api import demo as Demo
from ..api import demo_score as DemoScore
from ..forms.event import EventProfileForm, DemoConfigurationForm


@login_required
def dashboard(request):
    """Dashboard for admin."""
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('index')

    if request.method == 'GET':
        context = {
            'user': request.user,
            'demos': Demo.search(),
            'judges': User.search(is_judge=True),
            'is_debug': settings.DEBUG,
            'config_form': DemoConfigurationForm(instance=Event.get()),
        }
        return render(request, 'admin/dashboard.html', context)

    return redirect('dashboard')


@login_required
def edit_categories(request):
    """Page for editing categories."""
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('index')

    if request.method == 'GET':
        context = {
            'categories': Category.search().order_by('name'),
            'organizations': Organization.search().order_by('name'),
            'organizers_id': Event.get().id,
        }
        return render(request, 'admin/edit_categories.html', context)

    return redirect('edit_categories')


@login_required
def edit_organizations(request):
    """Page for editing organizations."""
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('index')

    if request.method == 'GET':
        context = {
            'categories': Category.search().order_by('name'),
            'organizations': Organization.search().order_by('name'),
            'organizers_id': Event.get().id,
        }
        return render(request, 'admin/edit_organizations.html', context)

    return redirect('edit_organizations')


@login_required
def edit_teams(request):
    """Page for editing teams."""
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('index')

    if request.method == 'GET':
        context = {
            'teams': Team.search(is_anchor=False).order_by('table', 'name')
        }
        return render(request, 'admin/edit_teams.html', context)

    return redirect('edit_teams')


@login_required
def edit_event(request):
    """Assign demos to judges.

    Only staff can assign demos.
    """
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('index')

    if request.method == 'GET':
        event = Event.get()
        context = {
            'form': EventProfileForm(instance=event),
            'event': event,
        }
        return render(request, 'admin/edit_event.html', context)
    elif request.method == 'POST':
        form = EventProfileForm(request.POST)
        if form.is_valid():
            kwargs = {
                'event_id': Event.get().id,
                'name': form.cleaned_data.get('name'),
                'organizers_id': form.cleaned_data.get('organizers').id,
            }
            Event.update(**kwargs)
        return redirect('edit_event')
    return redirect('edit_event')


@login_required
def normalize(request):
    """Page for running a judge normalization session.

    Allow organizer to create/update/delete "anchor" teams.
    The justification behind such a normalization session can be
    found in the README of this repo.
    """
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('index')

    if request.method == 'GET':
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
        return render(request, 'admin/anchors.html', context)
    return redirect('normalize')


@login_required
def assign_tables(request):
    """Assign tables to teams.

    Only staff can assign teams.
    """
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('index')

    if request.method == 'POST':
        teams = Team.search().order_by('id')
        num_digits = len(str(len(teams)))
        table_cnt = 1
        for team in teams:
            zeros_needed = num_digits - len(str(table_cnt))
            table_number = zeros_needed * '0' + str(table_cnt)
            Team.update(team.id, table=table_number)
            table_cnt += 1
        return redirect('dashboard')
    return redirect('dashboard')


@login_required
def statistics(request):
    """Assign tables to teams.

    Only staff can assign teams.
    """
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('index')

    if request.method == 'GET':
        context = {}

        judges = []
        for judge in User.search(is_judge=True):
            judges.append({
                'name': str(judge),
                'count': len(Demo.search(judge_id=judge.id))
            })
        context['judges'] = judges

        statistics = []

        num_judges = len(User.search(is_judge=True))
        num_demos = len(Demo.search())
        demos_per_judge = 0
        if num_judges > 0:
            demos_per_judge = num_demos / num_judges
        statistics.append({
            'name': 'Number of judges',
            'value': num_judges
        })
        statistics.append({
            'name': 'Number of demos',
            'value': num_demos
        })
        statistics.append({
            'name': 'Average demos per judge',
            'value': demos_per_judge
        })

        context['statistics'] = statistics
        return render(request, 'admin/statistics.html', context)
    return redirect('statistics')


@login_required
def scores(request):
    # TODO: move computation into POST request
    """Page for viewing and normalizing scores."""
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('index')

    if request.method == 'GET':
        context = {}

        teams = Team.search()
        team_scores = []
        for team in teams:
            team_demos = Demo.search(team_id=team.id)
            demo_totals = []
            for demo in team_demos:
                demo_totals.append(demo.raw_score)
            team_scores.append((sum(demo_totals) / len(demo_totals), team))

        rankings = sorted(team_scores, key=lambda i: i[0], reverse=True)

        score, winner = rankings[0]
        winning_scores = []
        for demo in Demo.search(team_id=winner.id):
            scores = DemoScore.search(demo_id=demo.id)
            winning_scores.append([score.value for score in scores])

        context['rankings'] = rankings
        context['winning_scores'] = winning_scores
        return render(request, 'admin/scores.html', context)
    return redirect('scores')
