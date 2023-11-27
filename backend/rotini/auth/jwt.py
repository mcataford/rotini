import datetime
import uuid

import django.conf

import jwt


def generate_token_for_user(user_id: int) -> str:
    """
    Generates an identity token for a given user.
    """
    token_data = {
        "exp": (datetime.datetime.now() + datetime.timedelta(seconds=120)).timestamp(),
        "user_id": user_id,
        "username": "yolo",
        "token_id": str(uuid.uuid4()),
    }

    return jwt.encode(
        token_data, django.conf.settings.JWT_SIGNING_SECRET, algorithm="HS256"
    )


def decode_token(
    token: str,
):
    """
    Decodes the given token.

    This may raise if the token is expired or invalid.
    """
    token_data = jwt.decode(
        token, django.conf.settings.JWT_SIGNING_SECRET, algorithms=["HS256"]
    )

    return token_data
