"""
Class declarations and constants for the auth module.
"""
import pydantic


class LoginRequestData(pydantic.BaseModel):
    """Payload for login requests"""

    username: str
    password: str


class CreateUserRequestData(pydantic.BaseModel):
    """Payload for user creation"""

    username: str
    password: str


class IdentityTokenData(pydantic.BaseModel):
    """Contents of an identity token"""

    exp: int
    user_id: int
    username: str
    token_id: str


class UsernameAlreadyExists(Exception):
    """Signals a unique constraint violation on username values"""
