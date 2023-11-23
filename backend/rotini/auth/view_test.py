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
