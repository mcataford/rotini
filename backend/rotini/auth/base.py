import pydantic


class LoginRequestData(pydantic.BaseModel):
    """Payload for login requests"""

    username: str
    password: str
