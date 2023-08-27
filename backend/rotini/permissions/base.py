import enum

import typing_extensions as typing


class Permissions(enum.Enum):
    """
    Enumeration of individual permission bits.

    Complex permissions are composed by combining these
    bits.
    """

    CAN_VIEW = 1 << 0
    CAN_DELETE = 1 << 1


class FilePermission(typing.TypedDict):
    """Representation of a permission applicable to a file+user pair"""

    file: str
    user: int
    value: typing.List[Permissions]
