# Create your views here.
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render


def home(request: WSGIRequest) -> HttpResponse:
    return render(request, "home.html", {"name": "main"})
