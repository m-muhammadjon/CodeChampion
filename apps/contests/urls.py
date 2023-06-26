from django.urls import path

from apps.contests import views

app_name = "contests"

urlpatterns = [
    path("contests", views.contest_list, name="contest_list"),
    path("contests/<int:pk>", views.contest_detail, name="contest_detail"),
]
