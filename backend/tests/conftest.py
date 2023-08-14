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
    with get_connection() as conn, conn.cursor() as cursor:
        cursor.execute("DELETE FROM files;")


@pytest.fixture(autouse=True)
def set_storage_path(tmp_path, monkeypatch):
    """
    Ensures that files stored by tests are stored
    in temporary directories.
    """

    files_dir = tmp_path / "files"
    files_dir.mkdir()

    monkeypatch.setattr(settings, "STORAGE_ROOT", str(files_dir))
