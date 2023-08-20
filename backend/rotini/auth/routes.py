from fastapi import APIRouter, Request, HTTPException

from use_cases.exceptions import DoesNotExist

import auth.use_cases as auth_use_cases

from .base import LoginRequestData

router = APIRouter(prefix="/auth")


@router.post("/users/")
async def create_user(request: Request):
    """
    POST /auth/users/

    {
        username: string
        password: string
    }

    201 { <UserData> }

        If the user is created successfully, the user object is returned.

    400 {}

        If the username already exists, or the password is not adequate,
        400 is returned.
    """
    body = await request.json()

    user = auth_use_cases.create_new_user(
        username=body["username"], raw_password=body["password"]
    )

    return user


@router.post("/sessions/")
async def log_in(payload: LoginRequestData):
    """
    Attempts to log a user in.

    200 { <User> }

        If the supplied credentials are correct, the user is returned.

    401 {}

        If the credentials are incorrect, immediate failure.
    """

    try:
        user = auth_use_cases.get_user(username=payload.username)
    except DoesNotExist as exc:
        raise HTTPException(status_code=401) from exc

    if not auth_use_cases.validate_password_for_user(user["id"], payload.password):
        raise HTTPException(status_code=401)

    return user
