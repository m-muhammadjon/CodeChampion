from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Exists, OuterRef
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST
from django_ratelimit.decorators import ratelimit

from apps.common.models import ProgrammingLanguage
from apps.problems.filters import AttemptFilter
from apps.problems.forms import AttemptForm
from apps.problems.models import Attempt, Problem


@ratelimit(key="ip", rate="10/m")
def problem_list(request: WSGIRequest) -> HttpResponse:
    request_user = request.user if request.user.is_authenticated else None
    problems = Problem.active.annotate(
        is_solved=Exists(Attempt.objects.filter(problem_id=OuterRef("id"), user=request_user, verdict="accepted")),
        is_attempted=Exists(Attempt.objects.filter(problem_id=OuterRef("id"), user=request_user)),
    ).all()
    return render(request, "problems/problem/problems.html", {"problems": problems, "name": "problems"})


def problem_detail(request: WSGIRequest, pk: int) -> HttpResponse:
    problem = Problem.objects.get(pk=pk)
    languages = ProgrammingLanguage.active.all()

    return render(
        request,
        "problems/problem/problem_detail.html",
        {
            "problem": problem,
            "languages": languages,
            "langs_json": {language.id: language.short_name for language in languages},
            "name": "problems",
            "sub_name": "problem",
        },
    )


@require_POST
@login_required
def submit_problem(request: WSGIRequest, pk: int) -> HttpResponse:
    form = AttemptForm(request.POST)
    if form.is_valid():
        attempt = form.save(commit=False)
        attempt.user = request.user
        attempt.problem_id = pk
        attempt.save()
        return redirect(f"{reverse('problems:problem_attempts', args=(pk,))}?mine=true")
    return HttpResponse("okay")


def problem_attempts(request: WSGIRequest, pk: int) -> HttpResponse:
    attempts = AttemptFilter(request.GET, Attempt.objects.filter(problem_id=pk), request=request)
    attempts = attempts.qs
    return render(
        request,
        "problems/problem/problem_attempts.html",
        {"attempts": attempts, "name": "problems", "sub_name": "attempts"},
    )


def attempt_list(request: WSGIRequest) -> HttpResponse:
    attempts = Attempt.objects.all()
    return render(request, "problems/attempt/attempt_list.html", {"attempts": attempts, "name": "attempts"})


def attempt_detail(request: WSGIRequest, pk: int) -> HttpResponse:
    attempt = Attempt.objects.get(pk=pk)
    if request.user != attempt.user:
        return redirect("base:home")  # TODO: move to attempts list
    return render(request, "problems/attempt/attempt_detail.html", {"attempt": attempt, "name": "attempts"})
