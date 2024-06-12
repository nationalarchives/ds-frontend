import os

from app.lib.util import strtobool


class Base(object):
    SECRET_KEY = os.environ.get("SECRET_KEY", "")

    DEBUG = strtobool(os.getenv("DEBUG", "False"))

    WAGTAIL_API_URL = os.environ.get("WAGTAIL_API_URL", "").rstrip("/")
    SEARCH_API_URL = os.environ.get("SEARCH_API_URL", "").rstrip("/")

    COOKIE_DOMAIN = os.environ.get("COOKIE_DOMAIN", "")

    CSP_IMG_SRC = os.environ.get("CSP_IMG_SRC", "'self'").split(",")
    CSP_SCRIPT_SRC = os.environ.get("CSP_SCRIPT_SRC", "'self'").split(",")
    CSP_STYLE_SRC = os.environ.get("CSP_STYLE_SRC", "'self'").split(",")
    CSP_FONT_SRC = os.environ.get("CSP_FONT_SRC", "'self'").split(",")
    CSP_CONNECT_SRC = os.environ.get("CSP_CONNECT_SRC", "'self'").split(",")
    CSP_MEDIA_SRC = os.environ.get("CSP_MEDIA_SRC", "'self'").split(",")
    FRAME_DOMAIN_ALLOW = os.environ.get("FRAME_DOMAIN_ALLOW", "")
    FORCE_HTTPS = strtobool(os.getenv("FORCE_HTTPS", "False"))

    CACHE_TYPE = "FileSystemCache"
    CACHE_DEFAULT_TIMEOUT = 0
    CACHE_IGNORE_ERRORS = True
    CACHE_DIR = os.environ.get("CACHE_DIR", "/tmp")

    BASE_DISCOVERY_URL = os.environ.get(
        "BASE_DISCOVERY_URL",
        "https://discovery.nationalarchives.gov.uk",
    ).rstrip("/")
    SEARCH_DISCOVERY_URL = os.environ.get(
        "SEARCH_DISCOVERY_URL",
        (
            os.environ.get(
                "BASE_DISCOVERY_URL",
                "https://discovery.nationalarchives.gov.uk",
            ).rstrip("/")
            + "/results/r"
        ),
    )
    SEARCH_WEBSITE_URL = os.environ.get(
        "SEARCH_WEBSITE_URL",
        "https://www.nationalarchives.gov.uk/search/results",
    )
    ARCHIVE_RECORDS_URL = os.environ.get(
        "ARCHIVE_RECORDS_URL",
        "https://discovery.nationalarchives.gov.uk/browse/r/h/",
    )

    GA4_ID = os.environ.get("GA4_ID", "")

    APPLY_REDIRECTS = strtobool(os.getenv("APPLY_REDIRECTS", "True"))


class Production(Base):
    ENVIRONMENT = "production"

    FORCE_HTTPS = strtobool(os.getenv("FORCE_HTTPS", "True"))

    # TODO: This invalidates the CSP nonces
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get("CACHE_DEFAULT_TIMEOUT", 300))


class Develop(Base):
    ENVIRONMENT = "develop"

    DEBUG = strtobool(os.getenv("DEBUG", "True"))

    CACHE_DEFAULT_TIMEOUT = int(os.environ.get("CACHE_DEFAULT_TIMEOUT", 1))


class Test(Base):
    ENVIRONMENT = "test"

    DEBUG = True

    WAGTAIL_API_URL = "http://wagtail.test/api/v2"
    SEARCH_API_URL = "http://search.test/api/v1"

    CACHE_TYPE = "SimpleCache"

    FORCE_HTTPS = False

    APPLY_REDIRECTS = False
