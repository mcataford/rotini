from fastapi import Request

from main import app

import auth.use_cases as auth_use_cases


@app.middleware("http")
async def authentication_middleware(request: Request, call_next):
    """
    Decodes Authorization headers if present on the request and sets
    identifying fields in the request state.

    This information is then leveraged by individual routes to determine
    authorization.
    """
    auth_header = request.headers.get("authorization")

    if auth_header is not None:
        _, token = auth_header.split(" ")
        decoded_token = auth_use_cases.decode_token(token)
        print(decoded_token)
        request.state.user = {
            "username": decoded_token["username"],
            "user_id": decoded_token["user_id"],
        }

    response = await call_next(request)
    return response
