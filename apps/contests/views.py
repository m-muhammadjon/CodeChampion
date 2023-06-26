from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render

from apps.contests.models import Contest


def contest_list(request: WSGIRequest) -> HttpResponse:
    contests = Contest.objects.filter(is_private=False).order_by("-start_date")
    return render(request, "contests/contest_list.html", {"contests": contests, "name": "contests"})


def contest_detail(request: WSGIRequest, pk: int) -> HttpResponse:
    contest = Contest.objects.get(pk=pk)
    return render(request, "contests/contest_detail.html", {"contest": contest, "name": "contests"})
