from fastapi.testclient import TestClient
import pytest

from rotini.main import app


@pytest.fixture()
def client():
    return TestClient(app)


def test_list_files(client):
    response = client.get("/files/")

    print(response)
