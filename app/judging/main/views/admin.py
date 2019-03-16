from collections import deque
import csv
from io import StringIO

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
def prejudging(request):
    """Page for configuration and setup before judging begins."""
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('index')

    if request.method == 'GET':
        context = {
            'user': request.user,
            'demos': Demo.search(),
            'organizations': Organization.search().order_by('name'),
            'organizers_id': Event.get().id,
            'judges': User.search(is_judge=True),
            'is_debug': settings.DEBUG,
            'config_form': DemoConfigurationForm(instance=Event.get()),
            'categories': Category.search().order_by('name')
        }
        return render(request, 'admin/prejudging.html', context)

    return redirect('prejudging')


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
def import_devpost(request):
    if request.method == 'GET':
        return render(request, 'admin/devpost.html')
    if request.method == 'POST':
        context = {}
        # source: https://www.pythoncircle.com/post/30/how-to-upload-and-process-the-csv-file-in-django/
        csv_file = request.FILES['devpost_csv']

        # check is a csv file
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Uploaded file must be a .csv')
            return redirect('import_devpost')

        # check if file too large
        if csv_file.multiple_chunks():
            messages.error(request, 'Uh oh, file ({:.2f}MB) too large, max (2.5MB)'.format(
                csv_file.size / (1000 * 1000)))
            return redirect('import_devpost')

        data = csv_file.read().decode("utf-8")
        reader = csv.reader(StringIO(data), csv.excel)
        headers = next(reader)
        for row in reader:
            prize = row[0]
            project_name = row[1]
            project_url = row[2]

            # get or create team
            teams = Team.search(link=project_url)
            if len(teams) == 0:
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
        return redirect('import_devpost')
    return redirect('import_devpost')


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
                scores = DemoScore.search(demo_id=demo.id)
                demo_total = 0
                for score in scores:
                    demo_total += score.criteria.weight * score.value
                demo_totals.append(demo_total)
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
