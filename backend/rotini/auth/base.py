import pydantic


class LoginRequestData(pydantic.BaseModel):
    """Payload for login requests"""

    username: str
    password: str


class CreateUserRequestData(pydantic.BaseModel):
    """Payload for user creation"""

    username: str
    password: str


class UsernameAlreadyExists(Exception):
    pass
