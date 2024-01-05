import typing
import json

import pytest
import freezegun

import django.urls
import django.contrib.auth
from django.test import Client
import identity.jwt
from identity.models import AuthenticationToken
from identity.serializers import UserSerializer

AuthUser = django.contrib.auth.get_user_model()


@pytest.fixture(name="create_user_request")
def fixture_create_user_request(auth_client):
    def _create_user_request(username: str, password: str):
        return auth_client.post(
            django.urls.reverse("auth-user-list"),
            {"username": username, "password": password},
        )

    return _create_user_request


@pytest.fixture(name="login_request")
def fixture_login_request(auth_client):
    def _login_request(username: str, password: str):
        return auth_client.post(
            django.urls.reverse("auth-session-list"),
            {"username": username, "password": password},
        )

    return _login_request


@pytest.fixture(name="logout_request")
def fixture_logout_request(auth_client):
    def _logout_request():
        return auth_client.delete(
            django.urls.reverse("auth-session-list"),
        )

    return _logout_request


@pytest.fixture(name="refresh_session_request")
def fixture_refresh_session_request(auth_client):
    def _refresh_session_request(refresh_token: typing.Optional[str] = None):
        data = {"refresh_token": refresh_token} if refresh_token else {}
        return auth_client.put(
            django.urls.reverse("auth-session-list"),
            json.dumps(data),
            content_type="application/json",
        )

    return _refresh_session_request


@pytest.fixture(name="get_session_request")
def fixture_get_session_request(auth_client):
    def _get_session_request():
        return auth_client.get(
            django.urls.reverse("auth-session-list"),
        )

    return _get_session_request


@pytest.fixture(name="get_current_user_request")
def fixture_get_current_user(auth_client):
    def _get_current_user_request(client: typing.Optional[Client] = None):
        chosen_client = client if client is not None else auth_client
        return chosen_client.get(django.urls.reverse("auth-user-list"))

    return _get_current_user_request


def test_create_new_user_returns_created_resource_on_success(create_user_request):
    mock_uname = "user"
    mock_pwd = "password"

    response = create_user_request(mock_uname, mock_pwd)

    created_user = AuthUser.objects.all().last()

    expected = {"username": mock_uname, "id": created_user.id}

    assert response.status_code == 201
    assert response.json() == expected


def test_create_new_user_returns_400_on_nonunique_username(create_user_request):
    mock_uname = "user"
    mock_pwd = "password"

    first = create_user_request(mock_uname, mock_pwd)
    second = create_user_request(mock_uname, mock_pwd)

    assert first.status_code == 201
    assert second.status_code == 400


def test_user_login_returns_valid_token_on_success(create_user_request, login_request):
    mock_uname = "user"
    mock_pwd = "password"

    creation_response = create_user_request(mock_uname, mock_pwd)

    login_response = login_request(mock_uname, mock_pwd)

    assert login_response.status_code == 201

    create_user_data = creation_response.json()

    assert "jwt" in login_response.cookies

    decoded_token = identity.jwt.decode_token(login_response.cookies["jwt"].value)
    assert decoded_token["user_id"] == create_user_data["id"]


def test_user_logout_ends_session(login_request, logout_request, test_user_credentials):
    login_response = login_request(
        test_user_credentials["username"], test_user_credentials["password"]
    )

    token = login_response.cookies["jwt"].value
    token_id = identity.jwt.decode_token(token)["token_id"]
    token_record = AuthenticationToken.objects.get(id=token_id)
    assert not token_record.revoked

    logout_response = logout_request()
    token_record.refresh_from_db()

    assert logout_response.status_code == 204
    assert token_record.revoked


def test_get_current_user_returns_data_if_authenticated(
    test_user, login_request, test_user_credentials, get_current_user_request
):
    login_request(test_user_credentials["username"], test_user_credentials["password"])

    response = get_current_user_request()
    test_user.refresh_from_db()
    assert response.status_code == 200
    assert response.json() == UserSerializer(test_user).data


def test_get_current_user_returns_403_if_unauthenticated(
    no_auth_client, get_current_user_request
):
    response = get_current_user_request(no_auth_client)

    assert response.status_code == 403


def test_get_session_returns_401_if_token_expired_past_threshold(
    test_user_credentials, login_request, get_session_request
):
    with freezegun.freeze_time("2012-01-01"):
        login_request(
            test_user_credentials["username"], test_user_credentials["password"]
        )

    response = get_session_request()

    assert response.status_code == 401


def test_get_session_returns_whether_token_should_be_refreshed(
    login_request, get_session_request, test_user_credentials
):
    login_request(test_user_credentials["username"], test_user_credentials["password"])

    response = get_session_request()

    assert response.status_code == 200
    assert response.json() == {"should_refresh": False}


def test_session_refresh_rejects_with_400_if_no_refresh_token(
    login_request,
    refresh_session_request,
    test_user_credentials,
):
    login_request(test_user_credentials["username"], test_user_credentials["password"])

    response = refresh_session_request()

    assert response.status_code == 400


def test_session_refresh_rejects_with_400_if_not_authenticated(refresh_session_request):
    response = refresh_session_request()

    assert response.status_code == 400


def test_session_refresh_attaches_new_token_to_response(
    login_request,
    refresh_session_request,
    test_user_credentials,
):
    login_response = login_request(
        test_user_credentials["username"], test_user_credentials["password"]
    )

    login_response_data = login_response.json()

    refresh_response = refresh_session_request(login_response_data["refresh_token"])

    refresh_response_data = refresh_response.json()

    assert refresh_response.status_code == 201
    assert (
        refresh_response_data["refresh_token"] != login_response_data["refresh_token"]
    )
    assert refresh_response.cookies["jwt"].value != login_response.cookies["jwt"].value
