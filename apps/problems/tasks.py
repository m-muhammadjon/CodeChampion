from celery import shared_task

from apps.problems.models import Attempt
from judges import check_cpp


@shared_task(
    name="check_attempt", autoretry_for=(Attempt.DoesNotExist,), retry_kwargs={"max_retries": 3, "countdown": 1}
)
def check_attempt(attempt_id: int) -> None:
    attempt = Attempt.objects.get(id=attempt_id)
    submission_result = None  # type: ignore

    language = attempt.language

    if language.short_name == "cpp":
        submission_result = check_cpp(attempt_id)  # noqa

    attempt.update_problem_statistics()
