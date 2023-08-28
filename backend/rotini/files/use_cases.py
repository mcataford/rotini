"""
File-related use cases.

Use cases and data structures defined in this file
manipulate file records in the database or represent them
after they have been read.
"""
import pathlib

import typing_extensions as typing

from db import get_connection
from settings import settings

from permissions.base import Permissions
from permissions.files import set_file_permission

from exceptions import DoesNotExist

from files.base import FileRecord


def create_file_record(path: str, size: int, owner_id: int) -> FileRecord:
    """
    Creates a record representing an uploaded file in the database.

    The record itself does not ensure that the file exists on disk, but just
    that it's tracked by the system.
    """
    inserted_id = None

    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO files (path, size) VALUES (%s, %s) RETURNING id", (path, size)
        )

        inserted_id = cursor.fetchone()[0]

    set_file_permission(inserted_id, owner_id, list(Permissions))

    filename = pathlib.Path(path).name

    return FileRecord(id=inserted_id, size=size, path=path, filename=filename)


def get_all_files_owned_by_user(user_id: int) -> typing.Tuple[FileRecord]:
    """
    Gets all the file records owned by the user.

    A file is considered owned if the user has all permissions on a given file. There
    can be more than one owner to a file, but all files must have an owner.
    """
    rows = None

    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            """SELECT
	            f.*
            from files f
            join permissions_files pf 
            on f.id = pf.file_id 
            where 
                pf.user_id = %s
                and pf.value = %s;""",
            (user_id, sum(p.value for p in Permissions)),
        )
        rows = cursor.fetchall()

    if rows is None:
        raise RuntimeError("Failed to get files.")

    return (
        FileRecord(
            id=row[0], path=row[1], size=row[2], filename=pathlib.Path(row[1]).name
        )
        for row in rows
    )


def get_file_record_by_id(file_id: str) -> typing.Optional[FileRecord]:
    """
    Fetches a single file by ID.

    If the ID doesn't correspond to a record, None is returned.
    """

    row = None
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM files WHERE id=%s;", (file_id,))
        row = cursor.fetchone()

    if row is None:
        return None

    return FileRecord(
        id=row[0], path=row[1], size=row[2], filename=pathlib.Path(row[1]).name
    )


def delete_file_record_by_id(file_id: str) -> typing.Union[typing.NoReturn, FileRecord]:
    """
    Deletes a single file by ID, including its presence in storage.

    If the ID doesn't correspond to a record, DoesNotExist is raised.
    """

    row = None
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DELETE FROM files WHERE id=%s RETURNING *;", (file_id,))
        row = cursor.fetchone()

    if row is None:
        raise DoesNotExist()

    pathlib.Path(pathlib.Path(settings.STORAGE_ROOT, row[1])).unlink()

    return FileRecord(
        id=row[0], path=row[1], size=row[2], filename=pathlib.Path(row[1]).name
    )
