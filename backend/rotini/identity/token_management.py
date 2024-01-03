from identity.models import AuthenticationToken


class UnregisteredTokenException(Exception):
    pass


class TokenAlreadyRevokedException(Exception):
    pass


def revoke_token_by_id(token_id: str):
    """
    Revokes a token given its identifier.

    If the token does not exist (i.e. no record for the id), an UnregisteredTokenException
    is raised.

    If the token is already revoked, an exception is also raised (double-revocation should not happen).
    """

    try:
        token_record = AuthenticationToken.objects.get(id=token_id)
    except AuthenticationToken.DoesNotExist as e:
        raise UnregisteredTokenException("Token {token_id} not registered.") from e

    if token_record.revoked:
        raise TokenAlreadyRevokedException(f"Token {token_id} already revoked.")

    token_record.revoked = True
    token_record.save()
