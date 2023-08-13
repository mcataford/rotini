"""
File-related use cases.

Use cases and data structures defined in this file
manipulate file records in the database or represent them
after they have been read.
"""
import typing
import pathlib

from db import get_connection
from settings import settings


class DoesNotExist(Exception):
    """
    General purpose exception signalling a failure to find a database record.
    """


class FileRecord(typing.TypedDict):
    """
    Database record associated with a file tracked
    by the system.
    """

    id: str
    size: int
    path: str
    filename: str


def create_file_record(path: str, size: int) -> FileRecord:
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

    filename = pathlib.Path(path).name

    return FileRecord(id=inserted_id, size=size, path=path, filename=filename)


def get_all_file_records() -> typing.Tuple[FileRecord]:
    """
    Fetches all availables files from the database.
    """

    rows = None

    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM files;")
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
        pathlib.Path(pathlib.Path(settings.STORAGE_ROOT, row[1])).unlink()

    if row is None:
        raise DoesNotExist()

    return FileRecord(
        id=row[0], path=row[1], size=row[2], filename=pathlib.Path(row[1]).name
    )
