import os
import subprocess
import time

from apps.base.websocket import send_attempt_info_to_group
from apps.problems.models import Attempt, AttemptVerdictChoices, TestCase

# import psutil


def check_cpp(attempt_id: int) -> bool:
    os.makedirs("files/attempt", exist_ok=True)  # create directory if not exists
    attempt = Attempt.objects.get(id=attempt_id)
    uid = attempt.uuid
    f = open(f"files/attempt/{uid}.cpp", "w+")
    f.write(attempt.source_code)
    f.close()
    send_attempt_info_to_group(attempt.user_id, False, attempt_id, "Compiling", 0, 0, False)

    p1 = subprocess.run(f"g++ files/attempt/{uid}.cpp -o files/attempt/{uid}.exe", capture_output=True, shell=True)
    if p1.stderr:
        attempt.verdict = AttemptVerdictChoices.compilation_error
        attempt.error = str(p1.stderr.decode("UTF-8"))
        attempt.is_checked = True
        attempt.save()
        os.remove(f"files/attempt/{uid}.cpp")
        send_attempt_info_to_group(attempt.user_id, False, attempt_id, "Compilation error", 0, 0, True)
        return False
    else:
        k = 0
        tests = TestCase.objects.filter(problem=attempt.problem)
        max_time = 0
        # max_memory = 0

        for test in tests:
            k += 1
            input = bytes(test.input, "UTF-8")
            begin = time.time()
            p2 = subprocess.Popen(
                f"files/attempt/{uid}.exe",
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
            )
            # memory = psutil.Process(p2.pid).memory_info().rss
            # max_memory = max(max_memory, memory)
            send_attempt_info_to_group(attempt.user_id, False, attempt_id, f"Running #{k}", 0, int(0 / 1024), False)
            try:
                stdout, stderr = p2.communicate(input, timeout=attempt.problem.time_limit / 1000)
                end = time.time()
                max_time = max(max_time, int((end - begin) * 1000))
                if stderr:
                    attempt.verdict = AttemptVerdictChoices.runtime_error
                    attempt.error_test_case = k
                    attempt.time = max_time
                    attempt.is_checked = True
                    # attempt.memory = int(max_memory / 1024)
                    attempt.save()
                    os.remove(f"files/attempt/{uid}.cpp")
                    os.remove(f"files/attempt/{uid}.exe")
                    send_attempt_info_to_group(
                        attempt.user_id, False, attempt_id, f"Runtime error #{k}", max_time, int(0 / 1024), True
                    )
                    return False
                else:
                    # if memory > submission.problem.memory_limit * 1024 * 1024:
                    #     submission.verdict = SubmissionVerdictChoices.ml
                    #     submission.test_case = k
                    #     submission.time = max_time
                    #     submission.checked = True
                    #     submission.memory = int(max_memory / 1024)
                    #     submission.save()
                    #     os.remove(f"robo/files/{uid}.cpp")
                    #     os.remove(f"robo/files/{uid}.exe")
                    #     for i in [["attempt", "attempt.message"], [f"{submission.user.id}", "user_submission_info"]]:
                    #         send_attempt_info_to_group(
                    #             i[0],
                    #             i[1],
                    #             False,
                    #             submission_id,
                    #             f"Memory limit (test {k})",
                    #             max_time,
                    #             int(max_memory / 1024),
                    #             True,
                    #         )
                    #     return False

                    if stdout.decode("UTF-8").strip() != test.output:
                        attempt.verdict = AttemptVerdictChoices.wrong_answer
                        attempt.error_test_case = k
                        attempt.time = max_time
                        attempt.is_checked = True
                        # attempt.memory = int(max_memory / 1024)
                        attempt.save()
                        os.remove(f"files/attempt/{uid}.cpp")
                        os.remove(f"files/attempt/{uid}.exe")
                        send_attempt_info_to_group(
                            attempt.user_id, False, attempt_id, f"Wrong answer #{k}", max_time, int(0 / 1024), True
                        )
                        return False

            except subprocess.TimeoutExpired:
                end = time.time()
                max_time = max(max_time, int((end - begin) * 1000))
                attempt.verdict = AttemptVerdictChoices.time_limit_exceeded
                attempt.error_test_case = k
                attempt.time = max_time
                attempt.is_checked = True
                attempt.memory = int(0 / 1024)
                attempt.save()
                os.remove(f"files/attempt/{uid}.cpp")
                os.remove(f"files/attempt/{uid}.exe")
                send_attempt_info_to_group(
                    attempt.user_id, False, attempt_id, f"Time limit exceeded #{k}", max_time, int(0 / 1024), True
                )
                return False
        attempt.verdict = AttemptVerdictChoices.accepted
        attempt.time = max_time
        attempt.is_checked = True
        # attempt.memory = int(max_memory / 1024)
        attempt.save()
        os.remove(f"files/attempt/{uid}.cpp")
        os.remove(f"files/attempt/{uid}.exe")
        send_attempt_info_to_group(attempt.user_id, False, attempt_id, "Accepted", max_time, int(0 / 1024), True)
        return True


__all__ = ["check_cpp"]
