import pytest
import freezegun
import jwt

import auth.jwt


@freezegun.freeze_time("2012-01-01")
def test_generates_and_decodes_token_token():
    MOCK_USER_ID = 1
    token = auth.jwt.generate_token_for_user(MOCK_USER_ID)

    assert token is not None

    token_data = auth.jwt.decode_token(token)

    assert token_data["user_id"] == MOCK_USER_ID


def test_token_decode_fails_if_expired():
    MOCK_USER_ID = 1

    with freezegun.freeze_time("2012-01-01"):
        token = auth.jwt.generate_token_for_user(MOCK_USER_ID)

    assert token is not None

    with pytest.raises(jwt.ExpiredSignatureError):
        auth.jwt.decode_token(token)
