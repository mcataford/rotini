import uuid
import datetime

import pytest

from identity.token_management import (
    revoke_token_by_id,
    renew_token,
    UnregisteredTokenException,
    TokenAlreadyRevokedException,
    TokenCannotBeRefreshedException,
    InvalidRefreshTokenException,
)
from identity.models import AuthenticationToken
from identity.jwt import generate_token_for_user

pytestmark = pytest.mark.djangodb


def test_revoke_token_by_id_fails_if_token_not_on_record():
    with pytest.raises(UnregisteredTokenException):
        revoke_token_by_id(str(uuid.uuid4()))


def test_revoke_token_by_id_fails_if_token_already_revoked(test_user):
    token_record = AuthenticationToken.objects.create(
        user_id=test_user.id,
        expires_at=datetime.datetime.now(datetime.timezone.utc),
        revoked=True,
    )
    with pytest.raises(TokenAlreadyRevokedException):
        revoke_token_by_id(str(token_record.id))


def test_revoke_token_by_id_sets_token_as_revoked(test_user):
    token_record = AuthenticationToken.objects.create(
        user_id=test_user.id, expires_at=datetime.datetime.now(datetime.timezone.utc)
    )
    revoke_token_by_id(str(token_record.id))

    token_record.refresh_from_db()

    assert token_record.revoked


def test_renew_token_fails_if_not_on_record(test_user):
    token, _ = generate_token_for_user(user_id=test_user.id)
    with pytest.raises(UnregisteredTokenException):
        renew_token(token, str(uuid.uuid4()))


def test_renew_token_fails_if_revoked(test_user):
    token, token_data = generate_token_for_user(user_id=test_user.id)

    token_record = AuthenticationToken.objects.create(
        id=token_data["token_id"],
        user_id=test_user.id,
        expires_at=datetime.datetime.now(datetime.timezone.utc),
        revoked=True,
    )

    with pytest.raises(TokenCannotBeRefreshedException):
        renew_token(token, str(token_record.refresh_token))


def test_renew_token_fails_if_refresh_token_wrong(test_user):
    token, token_data = generate_token_for_user(user_id=test_user.id)
    AuthenticationToken.objects.create(
        id=token_data["token_id"],
        user_id=test_user.id,
        expires_at=datetime.datetime.now(datetime.timezone.utc),
    )

    with pytest.raises(InvalidRefreshTokenException):
        renew_token(token, str(uuid.uuid4()))


def test_renew_token_generates_a_new_token_for_the_same_user(test_user):
    token, token_data = generate_token_for_user(user_id=test_user.id)

    token_record = AuthenticationToken.objects.create(
        id=token_data["token_id"],
        user_id=test_user.id,
        expires_at=datetime.datetime.now(datetime.timezone.utc),
    )

    _, token_data, refresh_token = renew_token(token, str(token_record.refresh_token))

    new_token_record = AuthenticationToken.objects.get(id=token_data["token_id"])

    assert new_token_record.user_id == token_record.user_id
    assert str(new_token_record.refresh_token) == refresh_token


def test_renew_token_revokes_previous_token(test_user):
    token, token_data = generate_token_for_user(user_id=test_user.id)

    token_record = AuthenticationToken.objects.create(
        id=token_data["token_id"],
        user_id=test_user.id,
        expires_at=datetime.datetime.now(datetime.timezone.utc),
    )

    _, token_data, _ = renew_token(token, str(token_record.refresh_token))

    new_token_record = AuthenticationToken.objects.get(id=token_data["token_id"])

    token_record.refresh_from_db()

    assert token_record.revoked
    assert new_token_record.revoked is False
