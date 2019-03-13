from collections import deque
import re
import csv
from io import StringIO

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect


from .api import user as User
from .api import organization as Organization
from .api import event as Event
from .api import team as Team
from .api import category as Category
from .api import criteria as Criteria
from .api import criteria_label as CriteriaLabel
from .api import demo as Demo
from .api import demo_score as DemoScore
from .forms.registration import RegistrationForm
from .forms.profile import UpdateProfileForm
from .forms.evaluation import EvaluationForm


def index(request):
    """Landing page.

    If not logged in, then render page. Otherwise, redirect
    to the dashboard. Links to log in and register page.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'main/index.html')


def register(request):
    """Registration page for judges.

    Links to login page for users who already have an
    account. On successful registration, goes to profile
    page with a next to dashboard.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'GET':
        context = {'form': RegistrationForm()}
        return render(request, 'registration/register.html', context)
    elif request.method == 'POST':
        form = RegistrationForm(request.POST)
        if not form.is_valid():
            redirect('register')
        form.save()  # create user
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('dashboard')
    return redirect('register')


@login_required
def profile(request):
    """Profile creation/edit page for judges."""
    if request.method == 'GET':
        context = {'form': UpdateProfileForm(instance=request.user)}  # TODO: add form
        return render(request, 'judge/profile.html', context)
    elif request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        return redirect('profile')
    return redirect('profile')


@login_required
def dashboard(request):
    """Dashboard for judges.

    If not logged in, redirects to index. If logged in, but the
    profile is incomplete, redirect to profile. If logged in and
    the profile is complete, render page.
    """
    if not request.user.is_profile_complete():
        return redirect('profile')

    if request.method == 'GET':
        if request.user.is_staff or request.user.is_superuser:
            context = {
                'user': request.user,
                'demos': Demo.search(),
                'judges': User.search(is_judge=True),
            }
            return render(request, 'admin/dashboard.html', context)
        else:
            demos = Demo.search(judge_id=request.user.id)
            demo_queue = []
            past_demos = []
            for demo in demos:
                if Demo.completed(demo.id):
                    past_demos.append(demo)
                else:
                    demo_queue.append(demo)

            context = {
                'user': request.user,
                'demo_queue': demo_queue,
                'past_demos': past_demos,
            }
            return render(request, 'judge/dashboard.html', context)
    return redirect('dashboard')


@login_required
def evaluate(request):
    """Form judges use to evaluate submissions.

    If not logged in, redirects to index. If logged in, but the
    profile is incomplete, redirect to profile. Otherwise, render
    the page. However, if judging has not started, disallow any
    form submissions.
    """
    if request.method == 'GET':
        initial = {}
        if request.GET.get('team'):
            # Get team, if specified
            team_id = request.GET.get('team')
            teams = Team.search(team_id=team_id)
            if len(teams) > 0:
                team = teams[0]

                # Get any initial data
                initial['team'] = team.id
                demos = Demo.search(judge_id=request.user.id, team_id=team_id)
                if len(demos) > 0:
                    demo = demos[0]

                    demo_scores = DemoScore.search(demo_id=demo.id)
                    for demo_score in demo_scores:
                        field_name = 'criteria-{}'.format(demo_score.criteria.id)
                        initial[field_name] = demo_score.value

        form = EvaluationForm(initial=initial)
        context = {
            'form': form
        }
        return render(request, 'judge/evaluate.html', context)
    elif request.method == 'POST':
        # Parse scores
        scores = {}
        prog = re.compile('^criteria-\d+$')
        for key, score in request.POST.dict().items():
            if prog.match(key):
                criteria_id = int(key[len('criteria-'):])
                scores[criteria_id] = score

        # Ensure all parts are complete
        num_criteria_expected = len(Criteria.search())
        if len(scores) != num_criteria_expected:
            messages.error(request, 'All criteria must be graded')
            return redirect('evaluate')

        # Get or create demo
        judge_id = request.user.id
        team_id = request.POST.get('team')
        demos = Demo.search(judge_id=judge_id, team_id=team_id)
        if len(demos) > 0:
            demo = demos[0]
        else:
            demo = Demo.create(judge_id, team_id)
        
        # Assign scores in demo
        for criteria_id, score in scores.items():
            if not DemoScore.exists(demo.id, criteria_id):
                DemoScore.create(demo.id, criteria_id, score)
            else:
                demo_scores = DemoScore.search(demo_id=demo.id ,criteria_id=criteria_id)
                demo_score = demo_scores[0]
                DemoScore.update(demo_score.id, value=score)

        # TODO: submit demo if judging is open
        return redirect('dashboard')



@login_required
def assign_demos(request):
    """Assign demos to judges.
    
    Only staff can assign demos. There are a few rules to
    follow when assigning demos, listed below.

    Implemented
    - All teams must be seen by at least _1_ judge

    Not Implemented
    - Every judge must see at least _1_ team
    - No judge can see more than _20_ teams
    - Judges should get demos in as _few_ categories as possible.
    """
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard')

    if request.method == 'POST':
        teams = Team.search()
        judges = User.search(is_judge=True)

        team_q = deque(teams)
        judge_q = deque(judges)
        while len(team_q) > 0:
            team = team_q.pop()
            judge = judge_q.pop()
            if not Demo.exists(judge.id, team.id):
                Demo.create(judge.id, team.id)
            judge_q.appendleft(judge)

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
            messages.error(request, 'Uh oh, file ({:.2f}MB) too large, max (2.5MB)'.format(csv_file.size/(1000*1000)))
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
                    organizers = Organization.search(name='organizers')[0]
                    category = Category.create(name=prize, organization_id=organizers.id, is_opt_in=True)
                    messages.warning(request, '"{}" was created and assigned to "{}" by default'.format(prize, organizers.name))
                else:
                    category = categories[0]  # TODO: more robust edge case checking

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
            response['reason'] = 'Organization with ID {} not found'.format(org_id)
            return JsonResponse(response)

        original_name = orgs[0].name
        org = Organization.update(org_id, org_name)
        response['success'] = True
        response['updated'] = original_name != org.name
        response['reason'] = '"{}" changed to "{}"'.format(original_name, org.name)
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
        response['reason'] = 'New organization called {} created'.format(org.name)
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
            response['reason'] = 'Organization with ID {} not found'.format(org_id)
            return JsonResponse(response)

        Organization.delete(org_id)
        response['success'] = True
        return JsonResponse(response)
    return JsonResponse(response)


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
