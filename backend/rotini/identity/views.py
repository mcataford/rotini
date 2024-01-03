import logging
import datetime

import django.http
import django.contrib.auth
import rest_framework.views
import rest_framework.status

import identity.jwt
from identity.models import AuthenticationToken
from identity.token_management import revoke_token_by_id

AuthUser = django.contrib.auth.get_user_model()

logger = logging.getLogger(__name__)


class SessionListView(rest_framework.views.APIView):
    """
    Views handling authenticated user sessions.
    """

    def post(self, request: django.http.HttpRequest) -> django.http.HttpResponse:
        """
        Handles signing in for existing users.

        If valid credentials are provided, a token is included in the
        response that can then be used to make authenticated requests.

        The token in included in the response cookies.

        POST /auth/login/
        {
          "username": "testuser",
          "password": "password"
        }

        200: The token is included as part of response cookies.
        401: The credentials provided were incorrect.
        """
        credentials = {
            "username": request.data.get("username"),
            "password": request.data.get("password"),
        }

        user = django.contrib.auth.authenticate(**credentials)

        if user is not None:
            django.contrib.auth.login(request, user)

            token, token_data = identity.jwt.generate_token_for_user(user_id=user.id)

            token_tracker = AuthenticationToken.objects.create(
                id=token_data["token_id"],
                user_id=token_data["user_id"],
                expires_at=datetime.datetime.fromtimestamp(token_data["exp"]),
            )

            response = django.http.JsonResponse(
                {"refresh_token": token_tracker.refresh_token}, status=201
            )

            response.set_cookie(
                "jwt", value=token, secure=False, domain="localhost", httponly=False
            )

            return response

        return django.http.HttpResponse(status=401)

    def delete(self, request: django.http.HttpRequest) -> django.http.HttpResponse:
        """
        Logs out the requesting user.

        The token associated with the user's session is revoked
        and cannot be reused after this is called.
        """

        current_token_id = request.session.get("token_id", None)

        if current_token_id is None:
            return django.http.HttpResponse(status=400)

        revoke_token_by_id(current_token_id)
        django.contrib.auth.logout(request)

        return django.http.HttpResponse(status=204)


class UserListView(rest_framework.views.APIView):
    """
    Routes dealing with non-specific users (without IDs).
    """

    def post(self, request: django.http.HttpRequest) -> django.http.HttpResponse:
        """
        Allows the creation of new users.

        A username and password must be provided, the username must be unique across the system.
        """

        credentials = {
            "username": request.data.get("username"),
            "password": request.data.get("password"),
        }

        # TODO: Add tests for view.
        try:
            new_user = AuthUser.objects.create_user(
                credentials["username"], "", credentials["password"]
            )
            logger.info(
                "Created new user.",
                extra={"username": new_user.username, "id": new_user.id},
            )
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.exception(e)
            return django.http.HttpResponse(status=400)

        return django.http.JsonResponse(
            {"username": new_user.username, "id": new_user.id}, status=201
        )
