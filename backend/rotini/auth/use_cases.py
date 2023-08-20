"""
User-related use cases.

Functions in this file are focused on users and passwords.
"""
import datetime
import typing_extensions as typing

import argon2

from db import get_connection
from exceptions import DoesNotExist

import auth.base as auth_base

password_hasher = argon2.PasswordHasher()


class User(typing.TypedDict):
    """
    User representation.

    The password hash is never included in these records and should
    not leave the database.
    """

    id: int
    username: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    password_updated_at: datetime.datetime


def create_new_user(*, username: str, raw_password: str) -> User:
    """
    Creates a new user record given a username and password.

    The password is hashed (see `_hash_secret`) and the hash is stored.

    If successful, returns a dictionary representing the user.
    """
    password_hash = _hash_secret(raw_password)

    with get_connection() as connection, connection.cursor() as cursor:
        try:
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (%s, %s) RETURNING id, username",
                (username, password_hash),
            )
            returned = cursor.fetchone()
        except Exception as exc:
            raise auth_base.UsernameAlreadyExists() from exc

    inserted_id = returned[0]
    created_username = returned[1]

    return User(
        id=inserted_id,
        username=created_username,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        password_updated_at=datetime.datetime.now(),
    )


def _hash_secret(secret: str) -> str:
    """
    Produces a hash of the given secret.
    """
    return password_hasher.hash(secret)


def get_user(
    *, username: str = None, user_id: int = None
) -> typing.Union[typing.NoReturn, User]:
    """
    Retrieves a user record, if one exists, for the given user.

    Querying can be done via username or user ID. The first one supplied, in this
    order, is used and any other values are ignored.
    """
    with get_connection() as connection, connection.cursor() as cursor:
        if username is not None:
            cursor.execute(
                "SELECT id, username, created_at, updated_at, password_updated_at FROM users WHERE username = %s;",
                (username,),
            )
        elif user_id is not None:
            cursor.execute(
                "SELECT id, username, created_at, updated_at, password_updated_at FROM users WHERE id = %s",
                (user_id,),
            )

        fetched = cursor.fetchone()

    if fetched is None:
        raise DoesNotExist()

    return User(
        id=fetched[0],
        username=fetched[1],
        created_at=fetched[2],
        updated_at=fetched[3],
        password_updated_at=fetched[4],
    )


def validate_password_for_user(user_id: int, raw_password: str) -> bool:
    """
    Validates whether a password is correct for the given user.

    Always returns a boolean representing whether it was a match or not.
    """
    try:
        with get_connection() as connection, connection.cursor() as cursor:
            cursor.execute("SELECT password_hash FROM users WHERE id = %s", (user_id,))
            fetched = cursor.fetchone()

        current_secret_hash = fetched[0]
        return password_hasher.verify(current_secret_hash, raw_password)
    except Exception:  # pylint: disable=broad-exception-caught
        return False
