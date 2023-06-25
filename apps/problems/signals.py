import uuid

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from apps.problems.models import Attempt
from apps.problems.tasks import check_attempt


@receiver(pre_save, sender=Attempt)
def set_uuid(sender, instance, **kwargs) -> None:
    if not instance.uuid:
        instance.uuid = uuid.uuid4()


@receiver(post_save, sender=Attempt)
def check_submission(sender, instance, created, **kwargs) -> None:
    if created:
        print(instance.user_id)
        layer = get_channel_layer()
        async_to_sync(layer.group_send)(
            "attempt",
            {
                "type": "attempt.message",
                "created": True,
                "user_id": str(instance.user_id),
                "username": instance.user.username,
                "attempt_id": instance.id,
                "status": "Waiting",
                "problem_title": instance.problem.title,
                "language": instance.language.short_name,
                "created_at": timezone.make_naive(instance.created_at).strftime("%d.%m.%Y %H:%M"),
            },
        )

        check_attempt.delay(instance.id)
