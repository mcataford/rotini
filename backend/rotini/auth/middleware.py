import logging

import django.http
import django.contrib.auth

import auth.jwt

logger = logging.getLogger(__name__)

AuthUser = django.contrib.auth.get_user_model()


class JwtMiddleware:
    """
    Middleware that handles using credentials supplied via the authorization
    headers on requests to log users in seamlessly.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: django.http.HttpRequest) -> django.http.HttpResponse:
        authorization_header = request.META.get("HTTP_AUTHORIZATION")

        if authorization_header is not None:
            try:
                _, token = authorization_header.split(" ")
                decoded_token = auth.jwt.decode_token(token)

                logger.info("Token: %s\nDecoded token: %s", token, decoded_token)

                user = AuthUser.objects.get(pk=decoded_token["user_id"])

                request.user = user
            except Exception as e:  # pylint: disable=broad-exception-caught
                logger.exception(
                    e, extra={"authorization_provided": authorization_header}
                )
                return django.http.HttpResponse(status=401)

        return self.get_response(request)
