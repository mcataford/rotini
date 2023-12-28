import pytest
import django.http
import django.contrib.auth
import auth.middleware
import auth.jwt

AuthUser = django.contrib.auth.get_user_model()


class HttpRequestWithUser(django.http.HttpRequest):
    """HttpRequest type after user is added by middleware."""

    user: AuthUser


@pytest.fixture(name="jwt_middleware")
def fixture_jwt_middleware():
    def _noop(_: django.http.HttpRequest):
        return django.http.HttpResponse()

    return auth.middleware.JwtMiddleware(_noop)


def test_middleware_does_not_append_user_details_to_request_if_invalid_credentials(
    jwt_middleware,
):
    """If authorization headers are present but cannot be validated, no user details."""
    mock_request = HttpRequestWithUser()

    mock_request.COOKIES["jwt"] = "notatoken"

    jwt_middleware(mock_request)

    assert not hasattr(mock_request, "user")


def test_middleware_adds_user_to_request_in_if_valid_token(
    jwt_middleware, test_user_credentials
):
    """If authorization headers are present and contain a valid JWT, sets user on request."""
    mock_request = HttpRequestWithUser()
    test_user = AuthUser.objects.get(username=test_user_credentials["username"])
    token = auth.jwt.generate_token_for_user(test_user.id)
    mock_request.COOKIES["jwt"] = token

    jwt_middleware(mock_request)

    assert mock_request.user == test_user
