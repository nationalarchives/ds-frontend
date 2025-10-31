import json
from urllib.parse import unquote

from flask import current_app, request


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
