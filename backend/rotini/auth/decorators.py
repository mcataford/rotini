import functools

import fastapi


def requires_logged_in(func):
    """
    Returns a 401 if the request received does not specify a logged
    in user in its state.

    The state is added through auth.middleware functionality.

    Note that this requires the endpoint to be aware of the fastapi.Request
    keyword argument passed to it.
    """

    @functools.wraps(func)
    async def wrapper(*, request: fastapi.Request, **kwargs):
        if not hasattr(request.state, "user"):
            raise fastapi.HTTPException(status_code=401)

        response = await func(**kwargs)
        return response

    return wrapper
