from collections import deque
import re

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
        context = {'form': form}
        return render(request, 'judge/profile.html', context)


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
            # initial = initial({})
            return render(request, 'judge/evaluate.html')

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
    teams = Team.search()
    judges = User.search(is_staff=False)

    team_q = deque(teams)
    judge_q = deque(judges)
    while len(team_q) > 0:
        team = team_q.pop()
        judge = judge_q.pop()
        if not Demo.exists(judge.id, team.id):
            Demo.create(judge.id, team.id)
        judge_q.appendleft(judge)

    return JsonResponse({
        'teams': list(teams.values()),
        'judges': list(judges.values()),
        'demos': list(Demo.search().values())
    })