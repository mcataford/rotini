"""
Global fixtures


"""
import django.test as django_test
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


@pytest.fixture(name="test_user", autouse=True)
def fixture_create_test_user(django_user_model, test_user_credentials):
    django_user_model.objects.create_user(**test_user_credentials)


"""
@pytest.fixture(name="test_user", autouse=True)
async def fixture_test_user(client_create_user, test_user_credentials):
    Sets up a test user using the `test_user_credentials` data.
    yield await client_create_user(test_user_credentials)
"""


@pytest.fixture(name="no_auth_client")
def fixture_no_auth_client() -> django_test.Client:
    """HTTP client without any authentication"""
    return django_test.Client()


@pytest.fixture(name="auth_client")
def fixture_auth_client(test_user_credentials) -> django_test.Client:
    """Authenticated HTTP client."""
    client = django_test.Client()
    assert client.login(**test_user_credentials)
    return client


"""
@pytest.fixture(name="jwt_client")
async def fixture_jwt_client(client_log_in, test_user_credentials):
    response = await client_log_in(test_user_credentials)
    auth_header = response.headers["authorization"]

    async with httpx.AsyncClient(
        app=app, base_url="http://test", headers={"Authorization": auth_header}
    ) as client:
        yield client


@pytest.fixture(name="client_log_in")
def fixture_client_log_in(no_auth_client):

    async def _client_log_in(credentials):
        return await no_auth_client.post("/auth/sessions/", json=credentials)

    return _client_log_in


@pytest.fixture(name="client_create_user")
def fixture_client_create_user(no_auth_client):

    async def _client_create_user(credentials):
        return await no_auth_client.post("/auth/users/", json=credentials)

    return _client_create_user
"""
