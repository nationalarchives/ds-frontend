from flask import request
from flask_caching import Cache

cache = Cache()


def cache_key_prefix():
    """Make a key that includes GET parameters."""
    return f"{request.full_path}{request.cookies.get('cookie_preferences_set' or '')}{request.cookies.get('theme' or '')}"


def rss_feedcache_key_prefix():
    return f"{request.full_path}{request.cookies.get('format' or '')}"
