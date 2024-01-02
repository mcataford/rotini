import logging

import django.http
import django.contrib.auth

import identity.jwt

logger = logging.getLogger(__name__)

AuthUser = django.contrib.auth.get_user_model()


class JwtMiddleware:
    """
    Middleware that handles using credentials supplied via request cookies
    carrying JWTs on requests to log users in seamlessly.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: django.http.HttpRequest) -> django.http.HttpResponse:
        """
        If a JWT cookie is attached to the request, its token value is
        retrieved, tentatively decoded and authentication details are
        added to the request data if available.

        On failure, no details are added.

        Views are expected to handle their own verification of
        whether the user details are adequate.
        """
        jwt_cookie = request.COOKIES.get("jwt")

        if jwt_cookie is not None:
            try:
                decoded_token = identity.jwt.decode_token(jwt_cookie)

                logger.info("Token: %s\nDecoded token: %s", jwt_cookie, decoded_token)

                user = AuthUser.objects.get(pk=decoded_token["user_id"])

                request.user = user
            except Exception as e:  # pylint: disable=broad-exception-caught
                logger.exception(e, extra={"authorization_provided": jwt_cookie})

        return self.get_response(request)
