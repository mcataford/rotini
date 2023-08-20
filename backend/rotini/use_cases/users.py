"""
User-related use cases.

Functions in this file are focused on users and passwords.
"""
import argon2

import datetime
import typing_extensions as typing

from db import get_connection
from use_cases.exceptions import DoesNotExist

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
    password_hash = _hash_secret(raw_password)

    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s) RETURNING id, username",
            (username, password_hash),
        )
        returned = cursor.fetchone()

    if returned is None:
        raise RuntimeError("Uh")

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
    return password_hasher.hash(secret)


def get_user(
    *, username: str = None, user_id: int = None
) -> typing.Union[typing.NoReturn, User]:
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
        raise RuntimeError("ho")

    return User(
        id=fetched[0],
        username=fetched[1],
        created_at=fetched[2],
        updated_at=fetched[3],
        password_updated_at=fetched[4],
    )


def validate_password_for_user(user_id: int, raw_password: str) -> bool:
    try:
        current_secret_hash = _get_password_hash_for_user(user_id)
        return password_hasher.verify(current_secret_hash, raw_password)
    except:
        return False


def _get_password_hash_for_user(user_id: int) -> str:
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT password_hash FROM users WHERE id = %s", (user_id,))
        fetched = cursor.fetchone()

    return fetched[0]
