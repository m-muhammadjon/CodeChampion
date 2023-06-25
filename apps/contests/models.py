from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

from apps.base.models import TimeStampedModel


class Contest(TimeStampedModel):
    title = models.CharField(max_length=255)
    description = RichTextUploadingField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    penalty_per_attempt = models.IntegerField(default=5)
    programming_languages = models.ManyToManyField("common.ProgrammingLanguage", related_name="contests")

    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class ContestParticipant(TimeStampedModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="participated_contests")
    contest = models.ForeignKey("contests.Contest", on_delete=models.CASCADE, related_name="participants")

    def __str__(self):
        return f"{self.user.username} - {self.contest}"


class ContestProblem(TimeStampedModel):
    contest = models.ForeignKey("contests.Contest", on_delete=models.CASCADE, related_name="problems")
    problem = models.ForeignKey("problems.Problem", on_delete=models.CASCADE, related_name="contests")
    symbol = models.CharField(max_length=3)
    point = models.IntegerField(default=1)
    attempted_users_count = models.IntegerField(default=0)
    solved_users_count = models.IntegerField(default=0)
    total_attempts_count = models.IntegerField(default=0)
    total_accepted_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.problem.title} - {self.contest.title}"

    class Meta:
        ordering = ["symbol"]
        unique_together = ["contest", "symbol"]


class Contestant(TimeStampedModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="contests")
    contest = models.ForeignKey("contests.Contest", on_delete=models.CASCADE, related_name="contestants")
    total_points = models.IntegerField(default=0)
    total_penalties = models.IntegerField(default=0)

    def __str__(self):
        return f"Contestant {self.user.username} - {self.contest.title}"


class ContestantProblemInfo(TimeStampedModel):
    contestant = models.ForeignKey("contests.Contestant", on_delete=models.CASCADE, related_name="problem_infos")
    contest_problem = models.ForeignKey("contests.ContestProblem", on_delete=models.CASCADE)
    attempt_count = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    penalties = models.IntegerField(default=0)
    is_solved = models.BooleanField(default=False)
    solved_at = models.DateTimeField(null=True, blank=True)
    is_first_solved = models.BooleanField(default=False)

    class Meta:
        ordering = ["contest_problem__symbol"]

    def get_clean_solved_time(self):
        if not self.is_solved:
            return None
        date = self.solved_at - self.contestant.contest.start_date
        return f"{date.days * 24 + date.seconds // 3600:02d}:{(date.seconds // 60) % 60:02d}:{date.seconds % 60:02d}"

    def get_clean_attempts_count(self):
        if not self.is_solved:
            if self.attempt_count == 1:
                return "-"
            return f"-{self.attempt_count}"
        else:
            if self.attempt_count == 1:
                return "+"
            return f"+{self.attempt_count - 1}"
