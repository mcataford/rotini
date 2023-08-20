from fastapi.testclient import TestClient
import pytest
import unittest.mock

from rotini.main import app
from rotini.db import get_connection

from settings import settings


@pytest.fixture(name="client")
def fixture_client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_database():
    """
    Empties all user tables between tests.
    """
    tables = ["files", "users"]

    with get_connection() as conn, conn.cursor() as cursor:
        for table in tables:
            cursor.execute("DELETE FROM " + table + ";")


@pytest.fixture(autouse=True)
def set_storage_path(tmp_path, monkeypatch):
    """
    Ensures that files stored by tests are stored
    in temporary directories.
    """

    files_dir = tmp_path / "files"
    files_dir.mkdir()

    monkeypatch.setattr(settings, "STORAGE_ROOT", str(files_dir))


@pytest.fixture(name="client_log_in")
def fixture_client_log_in(client):
    def _client_log_in(credentials):
        return client.post("/auth/sessions/", json=credentials)

    return _client_log_in


@pytest.fixture(name="client_create_user")
def fixture_client_create_user(client):
    def _client_create_user(credentials):
        return client.post("/auth/users/", json=credentials)

    return _client_create_user
