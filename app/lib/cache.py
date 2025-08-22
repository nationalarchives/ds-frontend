from flask import request
from flask_caching import Cache

cache = Cache()


def path_cache_key_prefix():
    return request.base_url


def page_cache_key_prefix():
    keys = [
        request.url,
        # request.cookies.get("cookie_preferences_set", "false"),
        # request.cookies.get("dontShowCookieNotice", "0"),
        request.cookies.get("theme", "0"),
    ]
    return "_".join(keys)


def rss_feed_cache_key_prefix():
    return f"{request.base_url}{request.args.get('format', '')}"
