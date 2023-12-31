import datetime
import uuid
import typing

import django.conf

import jwt


class TokenData(typing.TypedDict):
    exp: int
    user_id: int
    token_id: str


def generate_token_for_user(user_id: int) -> tuple[str, TokenData]:
    """
    Generates an identity token for a given user.

    Returns both the token data (decoded) and the encoding token string.

    The token expires in JWT_EXPIRATION seconds (defined in base.settings) and
    only contains the user's ID and a token ID that can be used to track the
    token once emitted.
    """

    token_data = {
        "exp": (
            datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(seconds=django.conf.settings.JWT_EXPIRATION)
        ).timestamp(),
        "user_id": user_id,
        "token_id": str(uuid.uuid4()),
    }

    return (
        jwt.encode(
            token_data, django.conf.settings.JWT_SIGNING_SECRET, algorithm="HS256"
        ),
        token_data,
    )


def decode_token(token: str, allow_expired: bool = False):
    """
    Decodes the given token.

    This may raise if the token is expired or invalid.

    If the `allow_expired` flag is truthy, the token is decoded even
    if the expiration claim is in the past.
    """
    options = {}

    if allow_expired:
        options["verify_exp"] = False

    token_data = jwt.decode(
        token,
        django.conf.settings.JWT_SIGNING_SECRET,
        algorithms=["HS256"],
        options=options,
    )

    return token_data
