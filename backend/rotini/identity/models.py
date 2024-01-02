import uuid
import datetime

from django.db import models
from django.conf import settings


class AuthenticationToken(models.Model):
    """
    Tracking record for authentication tokens generated
    by the application and not invalidated.

    Tokens contain their own expiration date (mirrored here with
    `expiration`). A token can be invalidated by the application
    by flipping the `revoked` flag - if truthy, the token bearing the id
    of the revoked token cannot be used and will be refused even if
    not expired yet.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # User associated with the token.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Refresh token associated with the token.
    refresh_token: str = models.UUIDField(null=False, default=uuid.uuid4)
    # Whether the token was revoked by the application.
    revoked: bool = models.BooleanField(default=False)
    created_at: datetime.datetime = models.DateTimeField(auto_now_add=True)
    updated_at: datetime.datetime = models.DateTimeField(auto_now=True)
    # Expiration date of the token, according to its content.
    expires_at: datetime.datetime = models.DateTimeField()
