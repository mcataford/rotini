from fastapi import APIRouter, Request, HTTPException

import use_cases.users as users_use_cases

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

    user = users_use_cases.create_new_user(
        username=body["username"], raw_password=body["password"]
    )

    return user


@router.post("/session/")
async def log_in(request: Request):
    """
    Attempts to log a user in.

    200 { <User> }

        If the supplied credentials are correct, the user is returned.

    401 {}

        If the credentials are incorrect, immediate failure.
    """

    body = await request.json()

    username = body["username"]
    password = body["password"]

    user = users_use_cases.get_user(username=username)

    if not users_use_cases.validate_password_for_user(user["id"], password):
        raise HTTPException(status_code=401)

    return user
