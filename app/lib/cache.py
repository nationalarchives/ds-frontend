from flask import request
from flask_caching import Cache

cache = Cache()


def page_cache_key_prefix():
    keys = [
        request.full_path,
        request.cookies.get("cookie_preferences_set") or "",
        request.cookies.get("theme") or "",
    ]
    return "_".join(keys)


def rss_feed_cache_key_prefix():
    return f"{request.full_path}{request.cookies.get('format') or ''}"
