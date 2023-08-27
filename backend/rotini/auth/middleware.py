"""
Authentication & authorization middleware logic.

This module is imported dynamically from `settings` to set up
middlewares with the `FastAPI` singleton.
"""
import logging

import jwt.exceptions
from fastapi import Request

from main import app

import auth.use_cases as auth_use_cases

logger = logging.getLogger(__name__)


@app.middleware("http")
async def authentication_middleware(request: Request, call_next):
    """
    Decodes Authorization headers if present on the request and sets
    identifying fields in the request state.

    This information is then leveraged by individual routes to determine
    authorization.
    """
    auth_header = request.headers.get("authorization")
    decoded_token = None

    if auth_header is not None:
        _, token = auth_header.split(" ")
        try:
            decoded_token = auth_use_cases.decode_token(token)
        except jwt.exceptions.ExpiredSignatureError as exc:
            logger.exception(exc)

    if decoded_token is not None:
        logger.info(decoded_token)
        request.state.user = {
            "username": decoded_token["username"],
            "user_id": decoded_token["user_id"],
        }

    response = await call_next(request)
    return response
