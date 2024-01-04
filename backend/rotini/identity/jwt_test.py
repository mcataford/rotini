import pytest
import freezegun
import jwt

import identity.jwt


@freezegun.freeze_time("2012-01-01")
def test_generates_and_decodes_token_token():
    MOCK_USER_ID = 1
    token, _ = identity.jwt.generate_token_for_user(MOCK_USER_ID)

    assert token is not None

    token_data = identity.jwt.decode_token(token)

    assert token_data["user_id"] == MOCK_USER_ID


def test_token_decode_fails_if_expired():
    MOCK_USER_ID = 1

    with freezegun.freeze_time("2012-01-01"):
        token, _ = identity.jwt.generate_token_for_user(MOCK_USER_ID)

    assert token is not None

    with pytest.raises(jwt.ExpiredSignatureError):
        identity.jwt.decode_token(token)


def test_token_decode_succeeds_if_expired_and_allow_expired_truthy():
    MOCK_USER_ID = 1

    with freezegun.freeze_time("2012-01-01"):
        token, token_data = identity.jwt.generate_token_for_user(MOCK_USER_ID)

    assert token is not None

    decoded_token = identity.jwt.decode_token(token, allow_expired=True)

    assert decoded_token is not None
    assert decoded_token == token_data
