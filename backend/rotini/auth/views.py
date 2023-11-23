import django.http
import django.contrib.auth
import rest_framework.views
import rest_framework.status

import auth.jwt


class LoginView(rest_framework.views.APIView):
    """
    Handles signing in for existing users.

    If valid credentials are provided, a token is included in the
    response that can then be used to make authenticated requests.

    POST /auth/login/
    {
      "username": "testuser",
      "password": "password"
    }

    200: The token is included as part of response cookies.
    401: The credentials provided were incorrect.
    """

    def post(self, request: django.http.HttpRequest) -> django.http.HttpResponse:
        credentials = {
            "username": request.data.get("username"),
            "password": request.data.get("password"),
        }

        user = django.contrib.auth.authenticate(**credentials)

        if user is not None:
            django.contrib.auth.login(request, user)

            token = auth.jwt.generate_token_for_user(user_id=user.id)
            response = django.http.HttpResponse(status=200)

            response.set_cookie("rotini_jwt", token)

            return response

        return django.http.HttpResponse(status=401)
