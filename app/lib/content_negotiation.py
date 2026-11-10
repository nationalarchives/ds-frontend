from functools import wraps

from flask import make_response, request


def get_requested_accept(options):
    """
    Pass the negotiated type as preferred_content_type and vary by Accept.
    """

    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            kwargs["preferred_content_type"] = request.accept_mimetypes.best_match(
                options
            )
            response = make_response(f(*args, **kwargs))
            response.vary.add("Accept")
            return response

        return wrapped

    return decorator
