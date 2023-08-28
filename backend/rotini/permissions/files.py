import typing_extensions as typing

from permissions.base import Permissions, FilePermission
from db import get_connection


def set_file_permission(
    file_id: str, user_id: int, permissions: typing.List[Permissions]
) -> FilePermission:
    """
    Given a file+user pair, creates a permission record with the
    provided permission list.
    """
    permission_value = sum(permission.value for permission in permissions)

    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO permissions_files (user_id, file_id, value) VALUES (%s, %s, %s) RETURNING id;",
            (user_id, file_id, permission_value),
        )
        inserted_row = cursor.fetchone()

    if inserted_row is None:
        raise RuntimeError("uh")

    return FilePermission(file=file_id, user=user_id, value=permissions)
