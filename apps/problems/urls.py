from django.urls import path

from apps.problems import views

app_name = "problems"

urlpatterns = [
    path("problems", views.problem_list, name="problem_list"),
    path("problems/<int:pk>", views.problem_detail, name="problem_detail"),
    path("problems/<int:pk>/submit", views.submit_problem, name="submit_problem"),
]
