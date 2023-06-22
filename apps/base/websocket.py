from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_attempt_info_to_group(
    user_id: int, created: bool, attempt_id: int, status: str, time: int, memory: int, is_finished: bool
) -> None:
    layer = get_channel_layer()
    for group_name, method in [("attempt", "attempt.message"), (f"{user_id}", "user_submission_info")]:
        async_to_sync(layer.group_send)(
            group_name,
            {
                "type": method,
                "created": created,
                "user_id": user_id,
                "attempt_id": attempt_id,
                "status": status,
                "time": time,
                "memory": memory,
                "is_finished": is_finished,
            },
        )
