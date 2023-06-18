from django.db import models


class TimeStampedModel(models.Model):
    """Base model with auto created and updated fields."""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("-created",)
