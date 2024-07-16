import json
import os

from app.lib.util import strtobool


class Features(object):
    FEATURE_PHASE_BANNER: bool = strtobool(
        os.getenv("FEATURE_PHASE_BANNER", "True")
    )


class Base(object):
    ENVIRONMENT: str = os.environ.get("ENVIRONMENT", "production")

    BUILD_VERSION: str = os.environ.get("BUILD_VERSION", "")
    TNA_FRONTEND_VERSION: str = ""
    with open(
        os.path.join(
            os.path.realpath(os.path.dirname(__file__)),
            "node_modules/@nationalarchives/frontend",
            "package.json",
        )
    ) as package_json:
        try:
            data = json.load(package_json)
            TNA_FRONTEND_VERSION = data["version"] or ""
        except ValueError:
            pass

    SECRET_KEY: str = os.environ.get("SECRET_KEY", "")

    DEBUG: bool = strtobool(os.getenv("DEBUG", "False"))

    SENTRY_DSN: str = os.getenv("SENTRY_DSN", "")
    SENTRY_JS_ID: str = os.getenv("SENTRY_JS_ID", "")
    SENTRY_SAMPLE_RATE: float = float(os.getenv("SENTRY_SAMPLE_RATE", "1.0"))

    WAGTAIL_API_URL: str = os.environ.get("WAGTAIL_API_URL", "").rstrip("/")
    SEARCH_API_URL: str = os.environ.get("SEARCH_API_URL", "").rstrip("/")

    COOKIE_DOMAIN: str = os.environ.get("COOKIE_DOMAIN", "")
    SESSION_COOKIE_DOMAIN: str | None = COOKIE_DOMAIN or None

    CSP_IMG_SRC: list[str] = os.environ.get("CSP_IMG_SRC", "'self'").split(",")
    CSP_SCRIPT_SRC: list[str] = os.environ.get(
        "CSP_SCRIPT_SRC", "'self'"
    ).split(",")
    CSP_SCRIPT_SRC_ELEM: list[str] = os.environ.get(
        "CSP_SCRIPT_SRC_ELEM", "'self'"
    ).split(",")
    CSP_STYLE_SRC: list[str] = os.environ.get("CSP_STYLE_SRC", "'self'").split(
        ","
    )
    CSP_FONT_SRC: list[str] = os.environ.get("CSP_FONT_SRC", "'self'").split(
        ","
    )
    CSP_CONNECT_SRC: list[str] = os.environ.get(
        "CSP_CONNECT_SRC", "'self'"
    ).split(",")
    CSP_MEDIA_SRC: list[str] = os.environ.get("CSP_MEDIA_SRC", "'self'").split(
        ","
    )
    CSP_WORKER_SRC: list[str] = os.environ.get(
        "CSP_WORKER_SRC", "'self'"
    ).split(",")
    CSP_FRAME_SRC: list[str] = os.environ.get("CSP_FRAME_SRC", "'self'").split(
        ","
    )
    CSP_FEATURE_FULLSCREEN: list[str] = os.environ.get(
        "CSP_FEATURE_FULLSCREEN", "'self'"
    ).split(",")
    CSP_FEATURE_PICTURE_IN_PICTURE: list[str] = os.environ.get(
        "CSP_FEATURE_PICTURE_IN_PICTURE", "'self'"
    ).split(",")
    FRAME_DOMAIN_ALLOW: str = os.environ.get("FRAME_DOMAIN_ALLOW", "")
    FORCE_HTTPS: bool = strtobool(os.getenv("FORCE_HTTPS", "True"))

    CACHE_TYPE: str = "FileSystemCache"
    CACHE_DEFAULT_TIMEOUT: int = int(
        os.environ.get("CACHE_DEFAULT_TIMEOUT", "1")
    )
    CACHE_IGNORE_ERRORS: bool = True
    CACHE_DIR: str = os.environ.get("CACHE_DIR", "/tmp")
    CACHE_HEADER_DURATION: int = int(os.getenv("CACHE_HEADER_DURATION", "1"))

    DISCOVERY_URL: str = os.environ.get(
        "DISCOVERY_URL",
        "https://discovery.nationalarchives.gov.uk",
    ).rstrip("/")
    ARCHIVE_RECORDS_URL: str = os.environ.get(
        "SEARCH_DISCOVERY_URL",
        (f"{DISCOVERY_URL}/browse/r/h"),
    ).rstrip("/")
    SEARCH_DISCOVERY_URL: str = os.environ.get(
        "SEARCH_DISCOVERY_URL",
        (f"{DISCOVERY_URL}/results/r"),
    ).rstrip("/")
    SEARCH_WEBSITE_URL: str = os.environ.get(
        "SEARCH_WEBSITE_URL",
        "https://www.nationalarchives.gov.uk/search/results",
    ).rstrip("/")

    GA4_ID: str = os.environ.get("GA4_ID", "")

    APPLY_REDIRECTS: bool = strtobool(os.getenv("APPLY_REDIRECTS", "True"))


class Production(Base, Features):
    SENTRY_SAMPLE_RATE = float(os.getenv("SENTRY_SAMPLE_RATE", "0.1"))

    CACHE_HEADER_DURATION = int(
        os.environ.get("CACHE_HEADER_DURATION", "604800")
    )  # 1 week

    # TODO: This invalidates the CSP nonces
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get("CACHE_DEFAULT_TIMEOUT", "300"))


class Staging(Base, Features):
    SENTRY_SAMPLE_RATE = float(os.getenv("SENTRY_SAMPLE_RATE", "0.25"))

    # TODO: This invalidates the CSP nonces
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get("CACHE_DEFAULT_TIMEOUT", "60"))


class Develop(Base, Features):
    DEBUG = strtobool(os.getenv("DEBUG", "True"))
    EXPLAIN_TEMPLATE_LOADING = True

    SENTRY_SAMPLE_RATE = float(os.getenv("SENTRY_SAMPLE_RATE", "1"))

    FORCE_HTTPS = strtobool(os.getenv("FORCE_HTTPS", "False"))


class Test(Base, Features):
    ENVIRONMENT = "test"

    DEBUG = True
    TESTING = True

    SENTRY_DSN = ""
    SENTRY_SAMPLE_RATE = 0

    WAGTAIL_API_URL = "http://wagtail.test/api/v2"
    SEARCH_API_URL = "http://search.test/api/v1"

    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 1
    CACHE_HEADER_DURATION = 0

    FORCE_HTTPS = False

    APPLY_REDIRECTS = False
