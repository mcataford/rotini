"""
Global fixtures


"""
from fastapi.testclient import TestClient
import httpx
import pytest

from main import app
from db import get_connection
from settings import settings


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture(autouse=False)
def reset_database():
    """Empties all user tables between tests."""
    tables = ["files", "users", "permissions_files"]

    with get_connection() as conn, conn.cursor() as cursor:
        for table in tables:
            cursor.execute("DELETE FROM " + table + ";")


@pytest.fixture(autouse=True)
async def set_storage_path(tmp_path, monkeypatch):
    """
    Ensures that files stored by tests are stored
    in temporary directories.
    """

    files_dir = tmp_path / "files"
    files_dir.mkdir()

    monkeypatch.setattr(settings, "STORAGE_ROOT", str(files_dir))


@pytest.fixture(name="test_user_credentials")
def fixture_test_user_creds():
    """
    Test user credentials.
    """
    return {"username": "testuser", "password": "testpassword"}


@pytest.fixture(name="test_user", autouse=True)
async def fixture_test_user(client_create_user, test_user_credentials):
    """
    Sets up a test user using the `test_user_credentials` data.
    """
    yield await client_create_user(test_user_credentials)


@pytest.fixture(name="no_auth_client")
async def fixture_no_auth_client():
    """HTTP client without any authentication"""
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(name="jwt_client")
async def fixture_jwt_client(client_log_in, test_user_credentials):
    """HTTP client with test user authentication via JWT"""
    response = await client_log_in(test_user_credentials)
    auth_header = response.headers["authorization"]

    async with httpx.AsyncClient(
        app=app, base_url="http://test", headers={"Authorization": auth_header}
    ) as client:
        yield client


@pytest.fixture(name="client_log_in")
def fixture_client_log_in(no_auth_client):
    """Logs in as the provided user"""

    async def _client_log_in(credentials):
        return await no_auth_client.post("/auth/sessions/", json=credentials)

    return _client_log_in


@pytest.fixture(name="client_create_user")
def fixture_client_create_user(no_auth_client):
    """Creates a new user given credentials"""

    async def _client_create_user(credentials):
        return await no_auth_client.post("/auth/users/", json=credentials)

    return _client_create_user
