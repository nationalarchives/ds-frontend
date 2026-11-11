from functools import wraps

from flask import g, make_response, request

from app.error_pages.routes import not_acceptable_error


def disallow_markdown(f):
    """Require HTML for this renderer and prevent subsequent Markdown conversion."""

    @wraps(f)
    def wrapped(*args, **kwargs):
        g.markdown_disabled = True
        if request.headers.get("Accept") and not request.accept_mimetypes["text/html"]:
            return not_acceptable_error()
        return f(*args, **kwargs)

    return wrapped


def get_requested_accept(options):
    """
    Pass the negotiated type as preferred_content_type and vary by Accept.
    """

    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            requested_accept = request.headers.get("Accept")
            preferred_content_type = request.accept_mimetypes.best_match(options)
            if requested_accept and preferred_content_type is None:
                response = make_response(not_acceptable_error())
            else:
                kwargs["preferred_content_type"] = preferred_content_type
                response = make_response(f(*args, **kwargs))
            if response.status_code == 406:
                response.cache_control.clear()
                response.cache_control.no_store = True
            response.vary.add("Accept")
            return response

        return wrapped

    return decorator
