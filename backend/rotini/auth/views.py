import django.http as django_http
import django.contrib.auth as django_auth
import rest_framework.views as drf_views
import rest_framework.status as drf_status

import auth.jwt as jwt_utils


class LoginView(drf_views.APIView):
    def post(self, request: django_http.HttpRequest) -> django_http.HttpResponse:
        credentials = {
            "username": request.data.get("username"),
            "password": request.data.get("password"),
        }

        user = django_auth.authenticate(**credentials)

        if user is not None:
            django_auth.login(request, user)

            token = jwt_utils.generate_token_for_user(user_id=user.id)
            response = django_http.HttpResponse(status=drf_status.HTTP_200_OK)

            response.set_cookie("rotini_jwt", token)

            return response
        else:
            return django_http.HttpResponse(status=drf_status.HTTP_401_UNAUTHORIZED)
