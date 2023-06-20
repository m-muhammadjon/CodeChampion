from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_attempt_info_to_group(
    group_name: str, method: str, created: bool, id: int, verdict: str, time: int, memory: int, tugadi: bool
) -> None:
    layer = get_channel_layer()
    async_to_sync(layer.group_send)(
        group_name,
        {
            "type": method,
            "created": created,
            "id": id,
            "verdict": verdict,
            "time": time,
            "memory": memory,
            "tugadi": tugadi,
        },
    )
