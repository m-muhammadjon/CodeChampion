from django.contrib import admin

from apps.contests.models import (Contest, Contestant, ContestantProblemInfo,
                                  ContestParticipant, ContestProblem)


class ContestProblemInline(admin.StackedInline):
    model = ContestProblem
    extra = 1


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    list_display = ["title", "start_date", "end_date", "is_private", "is_rated"]
    list_filter = ["is_private", "is_rated"]
    search_fields = ["title"]
    inlines = [ContestProblemInline]


@admin.register(ContestParticipant)
class ContestParticipantAdmin(admin.ModelAdmin):
    list_display = ["user", "contest"]
    list_filter = ["contest"]
    search_fields = ["user__username"]


class ContestantProblemInfoInline(admin.StackedInline):
    model = ContestantProblemInfo
    extra = 1


@admin.register(Contestant)
class ContestantAdmin(admin.ModelAdmin):
    list_display = ["user", "contest", "total_points", "total_penalties"]
    list_filter = ["contest"]
    search_fields = ["user__username"]
    inlines = [ContestantProblemInfoInline]
