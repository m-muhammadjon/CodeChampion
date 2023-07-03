from celery import shared_task
from django.db.models import Sum

from apps.contests.models import (Contestant, ContestantProblemInfo,
                                  ContestProblem)
from apps.problems.models import Attempt, AttemptVerdictChoices
from judges import check_cpp


@shared_task(
    name="check_attempt", autoretry_for=(Attempt.DoesNotExist,), retry_kwargs={"max_retries": 3, "countdown": 1}
)
def check_attempt(attempt_id: int) -> None:
    attempt = Attempt.objects.get(id=attempt_id)
    submission_result = None  # type: ignore
    contest = attempt.contest

    language = attempt.language

    if language.short_name == "cpp":
        submission_result = check_cpp(attempt_id)  # noqa

    attempt.update_problem_statistics()

    if contest:
        contestant, _ = Contestant.objects.get_or_create(user=attempt.user, contest=attempt.contest)
        contest_problem = ContestProblem.objects.get(contest=attempt.contest, problem=attempt.problem)
        contestant_problem_info, _ = ContestantProblemInfo.objects.get_or_create(
            contestant=contestant, contest_problem=contest_problem
        )
        for _contest_problem in contest.problems.all():
            ContestantProblemInfo.objects.get_or_create(contestant=contestant, contest_problem=_contest_problem)

        # Checks if the user solved the problem for the first time
        if submission_result and not contestant_problem_info.is_solved:
            contestant_problem_info.points = contest_problem.point
            contestant_problem_info.penalties = (
                contestant_problem_info.attempt_count * contest.penalty_per_attempt
                + (attempt.created_at - contest.start_date).total_seconds() // 60
            )
            contestant_problem_info.is_solved = True
            contestant_problem_info.solved_at = attempt.created_at

            # Checks if the user solved the problem first
            if not ContestantProblemInfo.objects.filter(
                contestant__contest=contest, contest_problem=contest_problem, is_solved=True
            ).exists():
                contestant_problem_info.is_first_solved = True

        # Calculate contestant problem's attempts count
        if not contestant_problem_info.is_solved:
            contestant_problem_info.attempt_count = contest.attempts.filter(
                user=attempt.user, problem=contest_problem.problem
            ).count()
        contestant_problem_info.save()

        contestant.total_penalties = contestant.problem_infos.aggregate(total_penalty=Sum("penalties"))["total_penalty"]
        contestant.total_points = contestant.problem_infos.aggregate(total_points=Sum("points"))["total_points"]
        contestant.save()

        contest_problem.attempted_users_count = (
            contest.attempts.filter(problem=contest_problem.problem).order_by("user").distinct("user").count()
        )
        contest_problem.solved_users_count = contestant.problem_infos.filter(
            contest_problem=contest_problem, is_solved=True
        ).count()
        contest_problem.total_attempts_count = contest.attempts.filter(problem=contest_problem.problem).count()
        contest_problem.total_accepted_count = contest.attempts.filter(
            problem=contest_problem.problem, verdict=AttemptVerdictChoices.accepted
        ).count()
        contest_problem.save()
