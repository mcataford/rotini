import uuid

from django.db import models
from django.conf import settings


class File(models.Model):
    """
    Represents a file tracked by the system.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    path = models.CharField(max_length=4096, null=False)
    size = models.IntegerField(null=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
