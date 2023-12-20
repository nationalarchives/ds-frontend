from flask import request


def cache_key_prefix():
    """Make a key that includes GET parameters."""
    return request.full_path
