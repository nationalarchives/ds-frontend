import json
import os

from app.lib.util import strtobool


class Features(object):
    FEATURE_PHASE_BANNER: bool = strtobool(os.getenv("FEATURE_PHASE_BANNER", "True"))
    FEATURE_NEW_ETC_HOMEPAGE: bool = strtobool(
        os.getenv("FEATURE_NEW_ETC_HOMEPAGE", "False")
    )
    FEATURE_LOGO_ADORNMENTS_CSS: str = os.getenv("FEATURE_LOGO_ADORNMENTS_CSS", "")
    FEATURE_LOGO_ADORNMENTS_JS: str = os.getenv("FEATURE_LOGO_ADORNMENTS_JS", "")


class Base(object):
    ENVIRONMENT_NAME: str = os.environ.get("ENVIRONMENT_NAME", "production")

    BUILD_VERSION: str = os.environ.get("BUILD_VERSION", "")
    TNA_FRONTEND_VERSION: str = ""
    try:
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
    except FileNotFoundError:
        pass

    SECRET_KEY: str = os.environ.get("SECRET_KEY", "")

    DEBUG: bool = strtobool(os.getenv("DEBUG", "False"))

    SENTRY_DSN: str = os.getenv("SENTRY_DSN", "")
    SENTRY_JS_ID: str = os.getenv("SENTRY_JS_ID", "")
    SENTRY_SAMPLE_RATE: float = float(os.getenv("SENTRY_SAMPLE_RATE", "0.1"))

    WAGTAIL_API_URL: str = os.environ.get("WAGTAIL_API_URL", "").rstrip("/")
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
    FORCE_HTTPS: bool = strtobool(os.getenv("FORCE_HTTPS", "True"))
    PREFERRED_URL_SCHEME: str = os.getenv("PREFERRED_URL_SCHEME", "https")

    CACHE_TYPE: str = os.environ.get("CACHE_TYPE", "FileSystemCache")
    CACHE_DEFAULT_TIMEOUT: int = int(os.environ.get("CACHE_DEFAULT_TIMEOUT", "900"))
    CACHE_IGNORE_ERRORS: bool = True
    CACHE_DIR: str = os.environ.get("CACHE_DIR", "/tmp")
    CACHE_REDIS_URL: str = os.environ.get("CACHE_REDIS_URL", "")

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
        "/blogs/",
        "/explore-the-collection/",
        "/help/",
        "/people/",
        "/whats-on/",
    ]


class Production(Base, Features):
    pass


class Staging(Base, Features):
    SENTRY_SAMPLE_RATE = float(os.getenv("SENTRY_SAMPLE_RATE", "1"))

    CACHE_DEFAULT_TIMEOUT = int(os.environ.get("CACHE_DEFAULT_TIMEOUT", "60"))


class Develop(Base, Features):
    SENTRY_SAMPLE_RATE = float(os.getenv("SENTRY_SAMPLE_RATE", "0"))

    CACHE_DEFAULT_TIMEOUT = int(os.environ.get("CACHE_DEFAULT_TIMEOUT", "1"))

    FEATURE_NEW_ETC_HOMEPAGE: bool = strtobool(
        os.getenv("FEATURE_NEW_ETC_HOMEPAGE", "True")
    )


class Test(Base, Features):
    ENVIRONMENT_NAME = "test"

    DEBUG = True
    TESTING = True
    EXPLAIN_TEMPLATE_LOADING = True

    SENTRY_DSN = ""
    SENTRY_SAMPLE_RATE = 0

    WAGTAIL_API_URL = "http://wagtail.test/api/v2"

    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 1

    FORCE_HTTPS = False
    PREFERRED_URL_SCHEME = "http"

    REDIRECT_WAGTAIL_ALIAS_PAGES = True
    SERVE_WAGTAIL_PAGE_REDIRECTIONS = True
    SERVE_WAGTAIL_EXTERNAL_REDIRECTIONS = True
