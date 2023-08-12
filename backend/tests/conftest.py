from fastapi.testclient import TestClient
import pytest

from rotini.main import app
from rotini.db import get_connection


@pytest.fixture(name="client")
def fixture_client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_database():
    with get_connection() as conn, conn.cursor() as cursor:
        cursor.execute("DELETE FROM files;")
