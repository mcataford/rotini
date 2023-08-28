"""
Authentication & authorization middleware logic.
"""
import logging

import jwt.exceptions
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

import auth.use_cases as auth_use_cases

logger = logging.getLogger(__name__)


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """
    Decodes Authorization headers if present on the request and sets
    identifying fields in the request state.

    This information is then leveraged by individual routes to determine
    authorization.
    """

    async def dispatch(self, request: Request, call_next):
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

        return await call_next(request)
