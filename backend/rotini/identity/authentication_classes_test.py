import datetime

import freezegun
import pytest
from django.http import HttpRequest

import identity.jwt
from identity.models import AuthenticationToken
from identity.authentication_classes import JwtAuthentication

pytestmark = pytest.mark.django_db


def test_jwt_authentication_accepts_valid_unrevoked_tokens(test_user):
    # An AuthenticationToken record exists for each issued token.
    auth_token, token_data = identity.jwt.generate_token_for_user(test_user.id)
    AuthenticationToken.objects.create(
        id=token_data["token_id"],
        user_id=token_data["user_id"],
        expires_at=datetime.datetime.fromtimestamp(token_data["exp"]),
    )

    request = HttpRequest()
    # Middleware would set up the session dict in a normal context.
    request.session = {}
    request.COOKIES["jwt"] = auth_token

    user, _ = JwtAuthentication().authenticate(request)

    assert user is not None
    assert user.id == token_data["user_id"]


def test_jwt_authentication_declines_expired_tokens(test_user):
    # Generating an expired token.
    with freezegun.freeze_time("2012-01-01"):
        auth_token, _ = identity.jwt.generate_token_for_user(test_user.id)

    request = HttpRequest()
    request.COOKIES["jwt"] = auth_token

    user, _ = JwtAuthentication().authenticate(request)

    assert user is None


def test_jwt_authentication_declines_revoked_tokens(test_user):
    auth_token, token_data = identity.jwt.generate_token_for_user(test_user.id)
    AuthenticationToken.objects.create(
        id=token_data["token_id"],
        user_id=token_data["user_id"],
        expires_at=datetime.datetime.fromtimestamp(token_data["exp"]),
        revoked=True,
    )
    request = HttpRequest()
    request.COOKIES["jwt"] = auth_token

    user, _ = JwtAuthentication().authenticate(request)

    assert user is None


def test_jwt_authentication_declines_invalid_tokens():
    request = HttpRequest()
    request.COOKIES["jwt"] = "notatoken"

    user, _ = JwtAuthentication().authenticate(request)

    assert user is None
