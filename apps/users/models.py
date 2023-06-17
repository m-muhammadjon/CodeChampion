from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django_resized import ResizedImageField


class User(AbstractUser):
    bio = models.TextField(null=True, blank=True)
    avatar = ResizedImageField(
        size=[300, 300],
        quality=100,
        upload_to="avatars",
        null=True,
        blank=True,
    )

    def get_status(self):
        if self.last_activity > timezone.now() - timezone.timedelta(minutes=2):
            return "online"
        return "offline"
