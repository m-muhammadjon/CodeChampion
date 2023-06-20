from apps.problems.models import Attempt
from judges import check_cpp


def check_attempt(attempt_id: int) -> None:
    attempt = Attempt.objects.get(id=attempt_id)
    submission_result = None  # type: ignore

    language = attempt.language

    if language.short_name == "cpp":
        submission_result = check_cpp(attempt_id)  # noqa
