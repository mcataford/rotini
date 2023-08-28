import pytest

pytestmark = pytest.mark.anyio


async def test_create_user_returns_201_on_success(client_create_user):
    credentials = {"username": "newuser", "password": "test"}
    response = await client_create_user(credentials)

    assert response.status_code == 201


async def test_create_user_with_nonunique_username_fails(client_create_user):
    credentials = {"username": "newuser", "password": "test"}
    await client_create_user(credentials)

    # Recreate the same user, name collision.
    response = await client_create_user(credentials)

    assert response.status_code == 400


@pytest.mark.parametrize(
    "credentials",
    [
        pytest.param({"username": "test"}, id="username_only"),
        pytest.param({"password": "test"}, id="password_only"),
        pytest.param({}, id="no_data"),
    ],
)
async def test_create_user_requires_username_and_password_supplied(
    client_create_user, credentials
):
    response = await client_create_user(credentials)

    assert response.status_code == 422


async def test_log_in_returns_200_and_user_on_success(
    client_log_in, test_user_credentials
):
    # The `test_user` fixture creates a user.

    response = await client_log_in(test_user_credentials)

    assert response.status_code == 200

    returned = response.json()

    assert returned["username"] == test_user_credentials["username"]


async def test_log_in_attaches_identity_token_to_response_on_success(
    client_log_in, test_user_credentials
):
    # This test specifically needs to inspect the JWT, hence the need to access
    # use case logic that is otherwise an implementation detail.

    import auth.use_cases as auth_use_cases

    response = await client_log_in(test_user_credentials)

    returned_auth = response.headers.get("authorization")
    token = returned_auth.split(" ")[1]  # Header of the form "Bearer <token>"

    assert (
        auth_use_cases.decode_token(token)["username"]
        == test_user_credentials["username"]
    )


async def test_log_in_returns_401_on_wrong_password(
    client_log_in, test_user_credentials
):
    response = await client_log_in(
        {"username": test_user_credentials["username"], "password": "sillystring"}
    )

    assert response.status_code == 401


async def test_log_in_returns_401_on_nonexistent_user(client_log_in):
    response = await client_log_in({"username": "notauser", "password": "sillystring"})

    assert response.status_code == 401


@pytest.mark.parametrize(
    "credentials",
    [
        pytest.param({"username": "test"}, id="username_only"),
        pytest.param({"password": "test"}, id="password_only"),
        pytest.param({}, id="no_data"),
    ],
)
async def test_log_in_returns_422_on_invalid_input(client_log_in, credentials):
    response = await client_log_in(credentials)

    assert response.status_code == 422
