import json
from datetime import UTC, datetime
from urllib.parse import unquote

from flask import current_app, request
from tna_utilities.currency import pretty_price_range as tna_pretty_price_range
from tna_utilities.datetime import rfc_822_date_format


def now_iso_8601():
    now = datetime.now(UTC)
    return now.strftime("%Y-%m-%dT%H:%M:%SZ")


def now_iso_8601_date():
    now = datetime.now(UTC)
    return now.date().isoformat()


def now_rfc_822():
    now = datetime.now(UTC)
    return rfc_822_date_format(now)


def pretty_price_range(a, b):
    return tna_pretty_price_range(float(a), float(b))


def cookie_preference(policy):
    if current_app.config["COOKIE_PREFERENCES_KEY"] in request.cookies:
        cookie_preferences = request.cookies[
            current_app.config["COOKIE_PREFERENCES_KEY"]
        ]
        preferences = json.loads(unquote(cookie_preferences))
        return preferences.get(policy, None)
    return None


def display_phase_banner():
    return any(
        request.path.startswith(uri)
        for uri in current_app.config.get("SHOW_PHASE_BANNER_ON_URIS", [])
    ) or (current_app.config["SHOW_PHASE_BANNER_ON_HOMEPAGE"] and request.path == "/")
