from django.urls import path

from apps.users import views

app_name = "users"

urlpatterns = [
    path("logout/", views.logout_view, name="logout"),
    path("login/", views.login_view, name="login"),
    # path("login/github/", views.github_login, name="github_login"),
    # path("complete/github/", views.github_login, name="github_login"),
]
