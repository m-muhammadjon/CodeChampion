from django.db import models
from django_resized import ResizedImageField

from apps.base.managers import ActiveManager
from apps.base.models import TimeStampedModel


class ProgrammingLanguage(TimeStampedModel):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=10)
    icon = ResizedImageField(
        size=[300, 300],
        quality=100,
        upload_to="programming_languages",
    )
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active = ActiveManager()

    def __str__(self):
        return self.name
