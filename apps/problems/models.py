from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _

from apps.base.managers import ActiveManager
from apps.base.models import TimeStampedModel


class AttemptVerdictChoices(models.TextChoices):
    waiting = "waiting", _("Waiting")
    compiling = "compiling", _("Compiling")
    running = "running", _("Running")
    accepted = "accepted", _("Accepted")
    wrong_answer = "wrong_answer", _("Wrong answer")
    time_limit_exceeded = "time_limit_exceeded", _("Time limit exceeded")
    presentation_error = "presentation_error", _("Presentation error")
    compilation_error = "compilation_error", _("Compilation error")
    memory_limit_exceeded = "memory_limit_exceeded", _("Memory limit exceeded")
    runtime_error = "runtime_error", _("Runtime error")


class Tag(TimeStampedModel):
    title = models.CharField(_("title"), max_length=256)
    slug = models.SlugField(_("slug"), max_length=256, unique=True, db_index=True)

    def __str__(self):
        return self.title


class Problem(TimeStampedModel):
    title = models.CharField(_("title"), max_length=256)
    description = RichTextUploadingField(_("description"))
    input_data = RichTextUploadingField(_("input data"))
    output_data = RichTextUploadingField(_("output data"))
    time_limit = models.PositiveIntegerField(_("time limit"))
    memory_limit = models.PositiveIntegerField(_("memory limit"))
    difficulty = models.PositiveSmallIntegerField(
        _("difficulty"), validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    tags = models.ManyToManyField("problems.Tag", related_name="problems", verbose_name=_("tags"))
    solved_users_count = models.PositiveIntegerField(_("solved users count"), default=0)
    accepted_submissions_count = models.PositiveIntegerField(_("accepted submissions count"), default=0)
    total_submissions_count = models.PositiveIntegerField(_("total submissions count"), default=0)
    acceptance_rate = models.FloatField(_("acceptance rate"), default=0)

    is_active = models.BooleanField(_("is active"), default=True)

    objects = models.Manager()
    active = ActiveManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("problems:problem_detail", args=[self.pk])

    def get_submission_url(self):
        return reverse("problems:submit_problem", args=[self.pk])

    class Meta:
        ordering = ("id",)
        verbose_name = _("Problem")
        verbose_name_plural = _("Problems")


class SampleTestCase(TimeStampedModel):
    problem = models.ForeignKey(
        "problems.Problem", on_delete=models.CASCADE, related_name="sample_test_cases", verbose_name=_("problem")
    )
    input = models.TextField(_("input data"))
    output = models.TextField(_("output data"))
    order = models.PositiveSmallIntegerField(_("order"), default=0)

    def __str__(self):
        return f"Sample test case of {self.problem.title}"

    class Meta:
        ordering = ["order"]
        verbose_name = _("Sample test case")
        verbose_name_plural = _("Sample test cases")


class TestCase(TimeStampedModel):
    problem = models.ForeignKey(
        "problems.Problem", on_delete=models.CASCADE, related_name="test_cases", verbose_name=_("problem")
    )
    input = models.TextField(_("input data"))
    output = models.TextField(_("output data"))
    order = models.PositiveSmallIntegerField(_("order"), default=0)

    def __str__(self):
        return f"Test case of {self.problem.title}"

    class Meta:
        unique_together = ["problem", "order"]
        ordering = ["order"]
        verbose_name = _("Test case")
        verbose_name_plural = _("Test cases")


class Attempt(TimeStampedModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="attempts", verbose_name=_("user"))
    problem = models.ForeignKey(
        "problems.Problem", on_delete=models.CASCADE, related_name="attempts", verbose_name=_("problem")
    )
    language = models.ForeignKey(
        "common.ProgrammingLanguage", on_delete=models.CASCADE, related_name="attempts", verbose_name=_("language")
    )
    source_code = models.TextField(_("source code"))
    uuid = models.UUIDField(_("uuid"), editable=False, null=True)
    verdict = models.CharField(_("verdict"), max_length=32, choices=AttemptVerdictChoices.choices, default="waiting")
    time = models.PositiveIntegerField(_("time"), default=0)
    memory = models.PositiveIntegerField(_("memory"), default=0)
    contest = models.ForeignKey(
        "contests.Contest",
        on_delete=models.CASCADE,
        related_name="attempts",
        verbose_name=_("contest"),
        null=True,
        blank=True,
    )
    error = models.TextField(_("error"), null=True, blank=True)
    error_test_case = models.PositiveIntegerField(_("error test case"), default=0)
    is_checked = models.BooleanField(_("is checked"), default=False)

    def __str__(self):
        return f"Attempt of {self.user.username} on {self.problem.title}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Attempt")
        verbose_name_plural = _("Attempts")

    def get_absolute_url(self):
        return reverse("problems:attempt_detail", args=[self.pk])

    def get_final_verdict(self) -> str:
        if self.is_checked and self.error_test_case != 0:
            return f"{self.get_verdict_display()} #{self.error_test_case}"
        return self.get_verdict_display()

    def update_problem_statistics(self) -> None:
        problem = self.problem
        problem.solved_users_count = (
            Attempt.objects.filter(problem=problem, verdict=AttemptVerdictChoices.accepted)
            .order_by("user")
            .distinct("user")
            .count()
        )
        problem.accepted_submissions_count = Attempt.objects.filter(
            problem=problem, verdict=AttemptVerdictChoices.accepted
        ).count()
        problem.total_submissions_count = Attempt.objects.filter(problem=problem).count()
        problem.acceptance_rate = round(problem.accepted_submissions_count / problem.total_submissions_count * 100, 3)
        problem.save()
