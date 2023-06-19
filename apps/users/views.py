from django.contrib.auth import authenticate, login, logout
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import redirect, render

from apps.users.forms import LoginForm


def logout_view(request: WSGIRequest) -> HttpResponse:
    logout(request)
    return redirect("users:home")


def login_view(request: WSGIRequest) -> HttpResponse:
    form = LoginForm(request.POST or None)
    if request.method == "POST":
        print(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd["email"], password=cd["password"])
            if user is not None and user.is_active:
                login(request, user)
                return redirect("users:home")
            else:
                return render(request, "users/auth/login.html", {"form": form})
        else:
            return render(request, "users/auth/login.html", {"form": form})
    return render(request, "users/auth/login.html", {"form": form})


def github_login(request: WSGIRequest) -> HttpResponse:
    return HttpResponse("github login")
