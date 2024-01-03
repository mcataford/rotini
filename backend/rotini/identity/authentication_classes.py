import logging

import django.contrib.auth
from rest_framework import authentication

import identity.jwt
from identity.models import AuthenticationToken

logger = logging.getLogger(__name__)

AuthUser = django.contrib.auth.get_user_model()


class RevokedTokenException(Exception):
    pass


class JwtAuthentication(authentication.BaseAuthentication):
    """
    Authentication class handling JWTs attached to requests via cookies.

    A JWT is only accepted if it's not expired (i.e. can be decoded) and if
    it has not been revoked (as per AuthenticationToken records). A revoked
    token is declined even if the token itself has not expired yet and would
    otherwise be valid.
    """

    def authenticate(self, request):
        jwt_cookie = request.COOKIES.get("jwt")

        # No JWT, no auth.
        if jwt_cookie is None:
            return None

        try:
            decoded_token = identity.jwt.decode_token(jwt_cookie)

            logger.info("Token: %s\nDecoded token: %s", jwt_cookie, decoded_token)

            user = AuthUser.objects.get(pk=decoded_token["user_id"])

            auth_token = AuthenticationToken.objects.get(id=decoded_token["token_id"])

            if auth_token.revoked:
                raise RevokedTokenException("Revoked tokens cannot be used")

            request.session["token_id"] = decoded_token["token_id"]

            return user, None

        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.exception(e, extra={"authorization_provided": jwt_cookie})
            return None, None
