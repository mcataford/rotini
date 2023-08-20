import pytest


@pytest.fixture(name="test_user_credentials")
def fixture_test_user_creds():
    """
    Test user credentials.
    """
    return {"username": "testuser", "password": "testpassword"}


@pytest.fixture(name="test_user", autouse=True)
def fixture_test_user(client_create_user, test_user_credentials):
    """
    Sets up a test user using the `test_user_credentials` data.
    """
    yield client_create_user(test_user_credentials)


def test_create_user_returns_201_on_success(client_create_user):
    credentials = {"username": "newuser", "password": "test"}
    response = client_create_user(credentials)

    assert response.status_code == 201


def test_create_user_with_nonunique_username_fails(client_create_user):
    credentials = {"username": "newuser", "password": "test"}
    client_create_user(credentials)

    # Recreate the same user, name collision.
    response = client_create_user(credentials)

    assert response.status_code == 400


@pytest.mark.parametrize(
    "credentials",
    [
        pytest.param({"username": "test"}, id="username_only"),
        pytest.param({"password": "test"}, id="password_only"),
        pytest.param({}, id="no_data"),
    ],
)
def test_create_user_requires_username_and_password_supplied(
    client_create_user, credentials
):
    response = client_create_user(credentials)

    assert response.status_code == 422


def test_log_in_returns_200_and_user_on_success(client_log_in, test_user_credentials):
    # The `test_user` fixture creates a user.

    response = client_log_in(test_user_credentials)

    assert response.status_code == 200

    returned = response.json()

    assert returned["username"] == test_user_credentials["username"]


def test_log_in_returns_401_on_wrong_password(client_log_in, test_user_credentials):
    response = client_log_in(
        {"username": test_user_credentials["username"], "password": "sillystring"}
    )

    assert response.status_code == 401


def test_log_in_returns_401_on_nonexistent_user(client_log_in):
    response = client_log_in({"username": "notauser", "password": "sillystring"})

    assert response.status_code == 401


@pytest.mark.parametrize(
    "credentials",
    [
        pytest.param({"username": "test"}, id="username_only"),
        pytest.param({"password": "test"}, id="password_only"),
        pytest.param({}, id="no_data"),
    ],
)
def test_log_in_returns_422_on_invalid_input(client_log_in, credentials):
    response = client_log_in(credentials)

    assert response.status_code == 422
