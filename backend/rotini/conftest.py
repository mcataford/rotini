"""
Global fixtures
"""

import django.contrib.auth
import django.test as django_test
import django.urls
import pytest


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture(name="test_user_credentials")
def fixture_test_user_creds():
    """
    Test user credentials.
    """
    return {"username": "testuser", "password": "testpassword"}


@pytest.fixture(name="test_user")
def fixture_test_user(test_user_credentials):
    """Fetches the test user record and returns it."""
    AuthUser = django.contrib.auth.get_user_model()

    return AuthUser.objects.get(username=test_user_credentials["username"])


@pytest.fixture(name="create_test_user", autouse=True)
def fixture_create_test_user(django_user_model, test_user_credentials):
    django_user_model.objects.create_user(**test_user_credentials)


@pytest.fixture(name="no_auth_client")
def fixture_no_auth_client() -> django_test.Client:
    """HTTP client without any authentication"""
    return django_test.Client()


@pytest.fixture(name="auth_client")
def fixture_auth_client(test_user_credentials) -> django_test.Client:
    """Authenticated HTTP client."""
    client = django_test.Client()
    response = client.post(
        django.urls.reverse("auth-session-list"), test_user_credentials
    )
    assert response.status_code == 201
    return client
