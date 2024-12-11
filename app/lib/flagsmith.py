import json
import os
import uuid
from urllib.parse import unquote

from app.lib.cache import cache
from flagsmith import Flagsmith
from flagsmith.models import DefaultFlag
from flask import current_app, request, session


def default_flag_handler(flag_name):
    default_values = current_app.config.get("DEFAULT_FLAGSMITH_VALUES")
    return DefaultFlag(enabled=False, value=default_values.get(flag_name, None))


flagsmith = Flagsmith(
    environment_key=os.environ.get("FLAGSMITH_ENV_KEY"),
    api_url=os.environ.get("FLAGSMITH_API_URL"),
    default_flag_handler=default_flag_handler,
    request_timeout_seconds=10,
)


def get_traits():
    return dict(
        theme=request.cookies.get("theme", "system"),
        cookie_policy=unquote(request.cookies.get("cookies_policy", "")),
    )


def traits_key():
    traits = get_traits()
    return ",".join(f"{trait}:{str(traits[trait])}" for trait in traits) + (
        f"-{session['user_id']}" if "user_id" in session else ""
    )


@cache.cached(key_prefix=traits_key, timeout=60)
def get_flags():
    if "user_id" in session:
        return flagsmith.get_identity_flags(
            identifier=session["user_id"], traits=get_traits()
        )
    if "cookies_policy" in request.cookies:
        current_cookies_policy = json.loads(
            unquote(request.cookies.get("cookies_policy"))
        )
        if current_cookies_policy["usage"]:
            session_id = uuid.uuid4().hex
            session["user_id"] = session_id
            return flagsmith.get_identity_flags(
                identifier=session["user_id"], traits=get_traits()
            )
    return flagsmith.get_environment_flags()


def is_feature_enabled(flag_name):
    flags = get_flags()
    return flags.is_feature_enabled(flag_name)


def get_flag_value(flag_name):
    flags = get_flags()
    return flags.get_feature_value(flag_name)


def get_all_flags():
    return get_flags().all_flags()
