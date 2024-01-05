import logging
import datetime
import json

from django.http import HttpResponse, JsonResponse, HttpRequest
import django.contrib.auth
import rest_framework.views
import rest_framework.status

import identity.jwt
from identity.models import AuthenticationToken
from identity.token_management import revoke_token_by_id, renew_token
from identity.serializers import UserSerializer
from identity.authentication_classes import JwtAuthenticationAllowExpired

AuthUser = django.contrib.auth.get_user_model()

logger = logging.getLogger(__name__)


class SessionListView(rest_framework.views.APIView):
    """
    Views handling authenticated user sessions.
    """

    authentication_classes = [JwtAuthenticationAllowExpired]

    def post(self, request: HttpRequest) -> HttpResponse:
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

            response = JsonResponse(
                {"refresh_token": token_tracker.refresh_token}, status=201
            )

            response.set_cookie(
                "jwt", value=token, secure=False, domain="localhost", httponly=False
            )

            return response

        return HttpResponse(status=401)

    def put(self, request: HttpRequest) -> HttpResponse:
        """
        Refreshes a session using a refresh token (provided via body).

        On success, returns a new authentication token via cookie and
        a new refresh token via response body.

        The previous auth+refresh token pair is invalidated and cannot be reused.
        """

        request_body = json.loads(request.body.decode("utf-8"))

        current_auth_token = request.COOKIES.get("jwt", None)
        current_refresh_token = request_body.get("refresh_token", None)
        if not current_auth_token or not current_refresh_token:
            return HttpResponse(status=400)

        new_token, _, new_refresh_token = renew_token(
            current_auth_token, current_refresh_token
        )

        response = JsonResponse({"refresh_token": new_refresh_token}, status=201)

        response.set_cookie(
            "jwt", value=new_token, secure=True, domain="localhost", httponly=False
        )

        return response

    def delete(self, request: HttpRequest) -> HttpResponse:
        """
        Logs out the requesting user.

        The token associated with the user's session is revoked
        and cannot be reused after this is called.
        """

        current_token_id = request.session.get("token_id", None)

        if request.session.get("expired", False):
            return HttpResponse(status=403)

        if current_token_id is None:
            return HttpResponse(status=400)

        revoke_token_by_id(current_token_id)
        django.contrib.auth.logout(request)

        return HttpResponse(status=204)

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Verifies if the current session is still valid.
        """

        current_token_id = request.session.get("token_id", None)

        token_record = AuthenticationToken.objects.get(id=current_token_id)

        if (
            token_record.expires_at + datetime.timedelta(minutes=5)
        ) < datetime.datetime.now(datetime.timezone.utc):
            return HttpResponse(status=401)

        should_refresh = datetime.datetime.now(
            datetime.timezone.utc
        ) > token_record.expires_at - datetime.timedelta(minutes=8)

        return JsonResponse({"should_refresh": should_refresh}, status=200)


class UserListView(rest_framework.views.APIView):
    """
    Routes dealing with non-specific users (without IDs).
    """

    queryset = AuthUser.objects.all()

    def post(self, request: HttpRequest) -> HttpResponse:
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
            return HttpResponse(status=400)

        return JsonResponse(
            {"username": new_user.username, "id": new_user.id}, status=201
        )

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Retrieves data about the current user.

        If the request is made unauthenticated, a 403 is returned.
        """

        if not request.user.is_authenticated:
            return HttpResponse(status=403)

        current_user = self.queryset.get(id=request.user.id)

        current_user_data = UserSerializer(current_user).data

        return JsonResponse(current_user_data, status=200)
