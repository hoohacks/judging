from collections import deque
import csv
from io import StringIO
from queue import PriorityQueue

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


@login_required
def assign_demos(request):
    """Assign demos to judges.

    Only staff can assign demos.
    """
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard')

    if request.method == 'POST':
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
                judges_for_category = User.search(is_judge=True, organization_id=category.organization.id)
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

        return redirect('dashboard')
    return redirect('dashboard')


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
def edit_organizations(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard')

    if request.method == 'GET':
        context = {
            'organizations': Organization.search().order_by('name')
        }
        return render(request, 'admin/edit_organizations.html', context)
    return redirect('edit_organizations')


@login_required
def assign_tables(request):
    """Assign tables to teams.

    Only staff can assign teams.
    """
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard')

    if request.method == 'POST':
        teams = Team.search().order_by('id')
        table_cnt = 1
        for team in teams:
            Team.update(team.id, table=table_cnt)
            table_cnt += 1
        return redirect('dashboard')
    return redirect('dashboard')
