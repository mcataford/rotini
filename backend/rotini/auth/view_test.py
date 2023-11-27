import auth.jwt

import pytest

import django.urls
import django.contrib.auth

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

    response_data = login_response.json()
    create_user_data = creation_response.json()

    assert "token" in response_data

    decoded_token = auth.jwt.decode_token(response_data["token"])

    assert decoded_token["user_id"] == create_user_data["id"]