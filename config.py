import os

from app.lib.util import strtobool


class Base(object):
    ENVIRONMENT = os.environ.get("ENVIRONMENT", "production")

    BUILD_VERSION = os.environ.get("BUILD_VERSION", "")

    SECRET_KEY = os.environ.get("SECRET_KEY", "")

    DEBUG = strtobool(os.getenv("DEBUG", "False"))

    SENTRY_DSN = os.getenv("SENTRY_DSN", "")
    SENTRY_JS_ID = os.getenv("SENTRY_JS_ID", "")
    SENTRY_SAMPLE_RATE = float(os.getenv("SENTRY_SAMPLE_RATE", "1.0"))

    WAGTAIL_API_URL = os.environ.get("WAGTAIL_API_URL", "").rstrip("/")
    SEARCH_API_URL = os.environ.get("SEARCH_API_URL", "").rstrip("/")

    COOKIE_DOMAIN = os.environ.get("COOKIE_DOMAIN", "")

    CSP_IMG_SRC = os.environ.get("CSP_IMG_SRC", "'self'").split(",")
    CSP_SCRIPT_SRC = os.environ.get("CSP_SCRIPT_SRC", "'self'").split(",")
    CSP_SCRIPT_SRC_ELEM = os.environ.get("CSP_SCRIPT_SRC_ELEM", "'self'").split(
        ","
    )
    CSP_STYLE_SRC = os.environ.get("CSP_STYLE_SRC", "'self'").split(",")
    CSP_FONT_SRC = os.environ.get("CSP_FONT_SRC", "'self'").split(",")
    CSP_CONNECT_SRC = os.environ.get("CSP_CONNECT_SRC", "'self'").split(",")
    CSP_MEDIA_SRC = os.environ.get("CSP_MEDIA_SRC", "'self'").split(",")
    CSP_WORKER_SRC = os.environ.get("CSP_WORKER_SRC", "'self'").split(",")
    CSP_FRAME_SRC = os.environ.get("CSP_FRAME_SRC", "'self'").split(",")
    FRAME_DOMAIN_ALLOW = os.environ.get("FRAME_DOMAIN_ALLOW", "")
    FORCE_HTTPS = strtobool(os.getenv("FORCE_HTTPS", "True"))

    CACHE_TYPE = "FileSystemCache"
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get("CACHE_DEFAULT_TIMEOUT", "1"))
    CACHE_IGNORE_ERRORS = True
    CACHE_DIR = os.environ.get("CACHE_DIR", "/tmp")
    CACHE_HEADER_DURATION = int(os.getenv("CACHE_HEADER_DURATION", "1"))

    DISCOVERY_URL = os.environ.get(
        "DISCOVERY_URL",
        "https://discovery.nationalarchives.gov.uk",
    ).rstrip("/")
    ARCHIVE_RECORDS_URL = os.environ.get(
        "SEARCH_DISCOVERY_URL",
        (f"{DISCOVERY_URL}/browse/r/h"),
    ).rstrip("/")
    SEARCH_DISCOVERY_URL = os.environ.get(
        "SEARCH_DISCOVERY_URL",
        (f"{DISCOVERY_URL}/results/r"),
    ).rstrip("/")
    SEARCH_WEBSITE_URL = os.environ.get(
        "SEARCH_WEBSITE_URL",
        "https://www.nationalarchives.gov.uk/search/results",
    ).rstrip("/")

    GA4_ID = os.environ.get("GA4_ID", "")

    APPLY_REDIRECTS = strtobool(os.getenv("APPLY_REDIRECTS", "True"))


class Production(Base):
    SENTRY_SAMPLE_RATE = float(os.getenv("SENTRY_SAMPLE_RATE", "0.1"))

    CACHE_HEADER_DURATION = int(
        os.environ.get("CACHE_HEADER_DURATION", "604800")
    )  # 1 week

    # TODO: This invalidates the CSP nonces
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get("CACHE_DEFAULT_TIMEOUT", "300"))


class Staging(Base):
    SENTRY_SAMPLE_RATE = float(os.getenv("SENTRY_SAMPLE_RATE", "0.25"))

    # TODO: This invalidates the CSP nonces
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get("CACHE_DEFAULT_TIMEOUT", "60"))


class Develop(Base):
    DEBUG = strtobool(os.getenv("DEBUG", "True"))

    SENTRY_SAMPLE_RATE = float(os.getenv("SENTRY_SAMPLE_RATE", "1"))

    FORCE_HTTPS = strtobool(os.getenv("FORCE_HTTPS", "False"))


class Test(Base):
    ENVIRONMENT = "test"

    DEBUG = True

    SENTRY_DSN = ""
    SENTRY_SAMPLE_RATE = 0

    WAGTAIL_API_URL = "http://wagtail.test/api/v2"
    SEARCH_API_URL = "http://search.test/api/v1"

    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 1
    CACHE_HEADER_DURATION = 0

    FORCE_HTTPS = False

    APPLY_REDIRECTS = False
