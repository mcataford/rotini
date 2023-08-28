import typing_extensions as typing


class FileRecord(typing.TypedDict):
    """
    Database record associated with a file tracked
    by the system.
    """

    id: str
    size: int
    path: str
    filename: str
