import json
import os

from app.lib.util import strtobool
from pydash import objects


class Features:
    FEATURE_PHASE_BANNER: bool = strtobool(os.getenv("FEATURE_PHASE_BANNER", "True"))
    FEATURE_LOGO_ADORNMENTS_CSS: str = os.getenv("FEATURE_LOGO_ADORNMENTS_CSS", "")
    FEATURE_LOGO_ADORNMENTS_JS: str = os.getenv("FEATURE_LOGO_ADORNMENTS_JS", "")


class Production(Features):
    ENVIRONMENT_NAME: str = os.environ.get("ENVIRONMENT_NAME", "production")
    BUILD_VERSION: str = os.environ.get("BUILD_VERSION", "")
    CONTAINER_IMAGE: str = os.environ.get("CONTAINER_IMAGE", "")

    TNA_FRONTEND_VERSION: str = ""
    try:
        package_lock_json_path = os.path.join(
            os.path.realpath(os.path.dirname(__file__)),
            "package-lock.json",
        )
        with open(package_lock_json_path) as package_json:
            data = json.load(package_json)
            TNA_FRONTEND_VERSION: str = objects.get(
                data, "packages.node_modules/@nationalarchives/frontend.version", ""
            )
    except Exception:
        # Error reading the version of TNA Frontend
        pass

    SECRET_KEY: str = os.environ.get("SECRET_KEY", "")

    DEBUG: bool = False

    SENTRY_DSN: str = os.getenv("SENTRY_DSN", "")
    SENTRY_JS_ID: str = os.getenv("SENTRY_JS_ID", "")
    SENTRY_SAMPLE_RATE: float = float(os.getenv("SENTRY_SAMPLE_RATE", "0.1"))

    WAGTAIL_API_URL: str = os.environ.get("WAGTAIL_API_URL", "").rstrip("/")
    WAGTAIL_API_KEY: str = os.environ.get("WAGTAIL_API_KEY", "")
    WAGTAIL_SITE_HOSTNAME: str = os.environ.get("WAGTAIL_SITE_HOSTNAME", "")
    WAGTAILAPI_LIMIT_MAX: int = int(os.environ.get("WAGTAILAPI_LIMIT_MAX", "20"))
    ITEMS_PER_SITEMAP: int = int(os.environ.get("ITEMS_PER_SITEMAP", "500"))
    ITEMS_PER_BLOG_FEED: int = int(os.environ.get("ITEMS_PER_BLOG_FEED", "50"))

    COOKIE_DOMAIN: str = os.environ.get("COOKIE_DOMAIN", "")

    CSP_IMG_SRC: list[str] = os.environ.get("CSP_IMG_SRC", "'self'").split(",")
    CSP_SCRIPT_SRC: list[str] = os.environ.get("CSP_SCRIPT_SRC", "'self'").split(",")
    CSP_STYLE_SRC: list[str] = os.environ.get("CSP_STYLE_SRC", "'self'").split(",")
    CSP_FONT_SRC: list[str] = os.environ.get("CSP_FONT_SRC", "'self'").split(",") + [
        "data:"  # video.js
    ]
    CSP_CONNECT_SRC: list[str] = os.environ.get("CSP_CONNECT_SRC", "'self'").split(",")
    CSP_MEDIA_SRC: list[str] = os.environ.get("CSP_MEDIA_SRC", "'self'").split(",")
    CSP_WORKER_SRC: list[str] = os.environ.get("CSP_WORKER_SRC", "'self'").split(",")
    CSP_FRAME_SRC: list[str] = os.environ.get("CSP_FRAME_SRC", "'self'").split(",")
    CSP_FRAME_ANCESTORS: list[str] = os.environ.get(
        "CSP_FRAME_ANCESTORS", "'self'"
    ).split(",")
    CSP_FEATURE_FULLSCREEN: list[str] = os.environ.get(
        "CSP_FEATURE_FULLSCREEN", "'self'"
    ).split(",")
    CSP_FEATURE_PICTURE_IN_PICTURE: list[str] = os.environ.get(
        "CSP_FEATURE_PICTURE_IN_PICTURE", "'self'"
    ).split(",")
    CSP_REPORT_URL: str = os.environ.get("CSP_REPORT_URL", "")
    if CSP_REPORT_URL:
        CSP_REPORT_URL += f"&sentry_release={BUILD_VERSION}" if BUILD_VERSION else ""
    FORCE_HTTPS: bool = strtobool(os.getenv("FORCE_HTTPS", "True"))
    PREFERRED_URL_SCHEME: str = os.getenv("PREFERRED_URL_SCHEME", "https")

    GA4_ID: str = os.environ.get("GA4_ID", "")

    REDIRECT_WAGTAIL_ALIAS_PAGES: bool = strtobool(
        os.getenv("REDIRECT_WAGTAIL_ALIAS_PAGES", "True")
    )
    SERVE_WAGTAIL_PAGE_REDIRECTIONS: bool = strtobool(
        os.getenv("SERVE_WAGTAIL_PAGE_REDIRECTIONS", "True")
    )
    SERVE_WAGTAIL_EXTERNAL_REDIRECTIONS: bool = strtobool(
        os.getenv("SERVE_WAGTAIL_EXTERNAL_REDIRECTIONS", "True")
    )

    SHOW_PHASE_BANNER_ON_URIS: list[str] = [
        "/about/",
        "/annual-report-and-accounts-2024-25/",
        "/blogs/",
        "/cookies/",
        "/explore-the-collection/",
        "/help/",
        "/image/",
        "/merlin/",
        "/mi5-official-secrets/",
        "/people/",
        "/professional-guidance-and-services/",
        "/whats-on/",
        "/video/",
    ]


class Staging(Production):
    DEBUG: bool = strtobool(os.getenv("DEBUG", "False"))

    SENTRY_SAMPLE_RATE = float(os.getenv("SENTRY_SAMPLE_RATE", "1"))


class Develop(Production):
    DEBUG: bool = strtobool(os.getenv("DEBUG", "False"))

    SENTRY_SAMPLE_RATE = float(os.getenv("SENTRY_SAMPLE_RATE", "0"))


class Test(Production):
    ENVIRONMENT_NAME = "test"

    DEBUG = True
    TESTING = True
    EXPLAIN_TEMPLATE_LOADING = True

    SENTRY_DSN = ""
    SENTRY_SAMPLE_RATE = 0

    WAGTAIL_API_URL = "http://wagtail.test/api/v2"

    FORCE_HTTPS = False
    PREFERRED_URL_SCHEME = "http"

    REDIRECT_WAGTAIL_ALIAS_PAGES = True
    SERVE_WAGTAIL_PAGE_REDIRECTIONS = True
    SERVE_WAGTAIL_EXTERNAL_REDIRECTIONS = True
