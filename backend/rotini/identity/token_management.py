import datetime

from identity.models import AuthenticationToken
from identity.jwt import decode_token, generate_token_for_user, TokenData


class UnregisteredTokenException(Exception):
    pass


class TokenAlreadyRevokedException(Exception):
    pass


class TokenCannotBeRefreshedException(Exception):
    pass


class InvalidRefreshTokenException(Exception):
    pass


def revoke_token_by_id(token_id: str):
    """
    Revokes a token given its identifier.

    If the token does not exist (i.e. no record for the id), an UnregisteredTokenException
    is raised.

    If the token is already revoked, an exception is also raised (double-revocation should not happen).
    """

    try:
        token_record = AuthenticationToken.objects.get(id=token_id)
    except AuthenticationToken.DoesNotExist as e:
        raise UnregisteredTokenException(f"Token {token_id} not registered.") from e

    if token_record.revoked:
        raise TokenAlreadyRevokedException(f"Token {token_id} already revoked.")

    token_record.revoked = True
    token_record.save()


def renew_token(token: str, refresh_token: str) -> tuple[str, TokenData, str]:
    """
    Given a token (expired or not) and its refresh token, creates a new
    token for the same user. The old token is invalidated.
    """

    token_data = decode_token(token, allow_expired=True)

    token_id = token_data["token_id"]

    try:
        token_record = AuthenticationToken.objects.get(id=token_id)
    except AuthenticationToken.DoesNotExist as e:
        raise UnregisteredTokenException(f"Token {token_id} not registered.") from e

    if token_record.revoked:
        raise TokenCannotBeRefreshedException(
            f"Token {token_id} is revoked and cannot be refreshed."
        )

    if refresh_token != str(token_record.refresh_token):
        raise InvalidRefreshTokenException(
            f"Refresh token {refresh_token} does not match records for {token_id}"
        )

    token_record.revoked = True
    token_record.save()

    new_token, token_data = generate_token_for_user(user_id=token_record.user_id)
    new_token_record = AuthenticationToken.objects.create(
        id=token_data["token_id"],
        user_id=token_data["user_id"],
        expires_at=datetime.datetime.fromtimestamp(token_data["exp"]),
    )

    return new_token, token_data, str(new_token_record.refresh_token)
