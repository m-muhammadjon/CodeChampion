from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from apps.contests.models import Contest, ContestParticipant
from apps.problems.forms import AttemptForm


def contest_list(request: WSGIRequest) -> HttpResponse:
    contests = Contest.objects.filter(is_private=False).order_by("-start_date")
    return render(request, "contests/contest_list.html", {"contests": contests, "name": "contests"})


def contest_detail(request: WSGIRequest, pk: int) -> HttpResponse:
    contest = Contest.objects.get(pk=pk)
    return render(
        request,
        "contests/contest_detail.html",
        {
            "contest": contest,
            "name": "contests",
            "first_problem": contest.problems.first().symbol,
            "user_is_registered": contest.user_is_registered(request.user),
            "now": timezone.now(),
        },
    )


@login_required()
def register_contest(request: WSGIRequest, pk: int) -> HttpResponse:
    contest = Contest.objects.get(pk=pk)
    ContestParticipant.objects.get_or_create(user=request.user, contest=contest)
    return redirect(contest.get_absolute_url())


def contest_problem_detail(request: WSGIRequest, pk: int, symbol: str) -> HttpResponse:
    contest = Contest.objects.get(pk=pk)
    problem = contest.problems.get(symbol=symbol)
    languages = contest.programming_languages.all()
    problems = contest.problems.all()
    return render(
        request,
        "contests/contest_problem.html",
        {
            "problem": problem,
            "name": "contests",
            "contest": contest,
            "problems": problems,
            "langs_json": {language.id: language.short_name for language in languages},
            "now": timezone.now(),
        },
    )


@require_POST
@login_required
def submit_contest_problem(request: WSGIRequest, pk: int, symbol: str) -> HttpResponse:
    form = AttemptForm(request.POST)
    if form.is_valid():
        contest_problem = Contest.objects.get(pk=pk).problems.get(symbol=symbol)
        attempt = form.save(commit=False)
        attempt.user = request.user
        attempt.problem = contest_problem.problem
        attempt.contest = contest_problem.contest
        attempt.save()
        return redirect(contest_problem.contest.get_absolute_url())
    print(form.errors)
    return HttpResponse("okay")


def contest_standings(request: WSGIRequest, pk: int) -> HttpResponse:
    contest = Contest.objects.get(pk=pk)
    contestants = contest.contestants.all().order_by("-total_points", "total_penalties")
    problems = contest.problems.all()
    return render(
        request,
        "contests/contest_standings.html",
        {
            "contest": contest,
            "name": "contests",
            "contestants": contestants,
            "problems": problems,
        },
    )
