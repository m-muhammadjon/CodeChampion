from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from apps.common.models import ProgrammingLanguage
from apps.problems.forms import AttemptForm
from apps.problems.models import Problem


def problem_list(request: WSGIRequest) -> HttpResponse:
    problems = Problem.active.all()
    return render(request, "problems/problems.html", {"problems": problems, "name": "problems"})


def problem_detail(request: WSGIRequest, pk: int) -> HttpResponse:
    problem = Problem.objects.get(pk=pk)
    languages = ProgrammingLanguage.active.all()

    return render(
        request,
        "problems/problem_detail.html",
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
    print(request.POST)
    form = AttemptForm(request.POST)
    if form.is_valid():
        attempt = form.save(commit=False)
        attempt.user = request.user
        attempt.problem_id = pk
        attempt.save()
        return HttpResponse("Submission keldi")
    return HttpResponse("okay")
