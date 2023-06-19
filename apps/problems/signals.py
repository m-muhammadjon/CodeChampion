import uuid

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from apps.problems.models import Attempt
from apps.problems.tasks import check_attempt


@receiver(pre_save, sender=Attempt)
def set_uuid(sender, instance, **kwargs) -> None:
    if not instance.uuid:
        instance.uuid = uuid.uuid4()


@receiver(post_save, sender=Attempt)
def check_submission(sender, instance, created, **kwargs) -> None:
    if created:
        check_attempt(instance.id)
