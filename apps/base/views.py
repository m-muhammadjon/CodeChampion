# Create your views here.
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render

from apps.contests.models import Contest
from apps.problems.models import Attempt, Problem
from apps.users.models import User


def home(request: WSGIRequest) -> HttpResponse:
    users_count = User.objects.count()
    problems_count = Problem.objects.count()
    attempts_count = Attempt.objects.count()
    contests_count = Contest.objects.count()

    return render(
        request,
        "home.html",
        {
            "name": "main",
            "users_count": users_count,
            "problems_count": problems_count,
            "attempts_count": attempts_count,
            "contests_count": contests_count,
        },
    )
