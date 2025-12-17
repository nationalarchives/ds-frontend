import json
from datetime import datetime
from urllib.parse import unquote

from flask import current_app, request


def now_iso_8601():
    now = datetime.now()
    now_date = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    return now_date


def now_iso_8601_date():
    now = datetime.now()
    now_date = now.strftime("%Y-%m-%d")
    return now_date


def now_rfc_822():
    now = datetime.now()
    now_date = now.strftime("%a, %-d %b %Y %H:%M:%S GMT")
    return now_date


def cookie_preference(policy):
    if "cookies_policy" in request.cookies:
        cookies_policy = request.cookies["cookies_policy"]
        preferences = json.loads(unquote(cookies_policy))
        return preferences[policy] if policy in preferences else None
    return None


def display_phase_banner():
    return any(
        request.path.startswith(uri)
        for uri in current_app.config.get("SHOW_PHASE_BANNER_ON_URIS", [])
    )
