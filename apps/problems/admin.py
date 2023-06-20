from django.contrib import admin

from apps.problems.models import (Attempt, Problem, SampleTestCase, Tag,
                                  TestCase)


class SampleTestCaseInline(admin.TabularInline):
    model = SampleTestCase
    extra = 0
    raw_id_fields = ("problem",)


class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 0
    raw_id_fields = ("problem",)


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "is_active",
        "difficulty",
        "solved_users_count",
        "accepted_submissions_count",
        "total_submissions_count",
        "acceptance_rate",
    )
    list_filter = ("is_active", "difficulty", "tags")
    search_fields = ("title",)
    inlines = (SampleTestCaseInline, TestCaseInline)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    search_fields = ("title", "slug")


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ("user", "problem", "verdict", "time", "memory")
    list_filter = ("verdict", "problem")
    search_fields = ("user__username", "problem__title")
    readonly_fields = ("uuid",)
