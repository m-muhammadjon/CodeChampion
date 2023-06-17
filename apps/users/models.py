from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField

from apps.users.managers import UserManager


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)

    bio = models.TextField(null=True, blank=True)
    avatar = ResizedImageField(
        size=[300, 300],
        quality=100,
        upload_to="avatars",
        null=True,
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def get_status(self):
        if self.last_activity > timezone.now() - timezone.timedelta(minutes=2):
            return "online"
        return "offline"
