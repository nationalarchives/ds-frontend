import os

from app.lib.util import strtobool


class Base(object):
    SECRET_KEY = os.environ.get("SECRET_KEY", "")

    DEBUG = strtobool(os.getenv("DEBUG", "False"))

    WAGTAIL_API_URL = os.environ.get("WAGTAIL_API_URL", "").rstrip("/")
    SEARCH_API_URL = os.environ.get("SEARCH_API_URL", "").rstrip("/")

    DOMAIN = os.environ.get("DOMAIN", "")
    MEDIA_DOMAIN = os.environ.get("MEDIA_DOMAIN", "")
    WAGTAIL_DOMAIN = os.environ.get("WAGTAIL_DOMAIN", "")
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

    # TODO: This invalidates the CSP nonces
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get("CACHE_DEFAULT_TIMEOUT", 300))

    FORCE_HTTPS = strtobool(os.getenv("FORCE_HTTPS", "True"))


class Develop(Base):
    ENVIRONMENT = "develop"

    DEBUG = strtobool(os.getenv("DEBUG", "True"))

    CACHE_DEFAULT_TIMEOUT = int(os.environ.get("CACHE_DEFAULT_TIMEOUT", 1))


class Test(Base):
    ENVIRONMENT = "test"

    DEBUG = True

    WAGTAIL_API_URL = "http://wagtail.test/api/v2"
    SEARCH_API_URL = "http://search.test/api/v1"

    DOMAIN = "http://localhost"
    MEDIA_DOMAIN = "http://media.test"

    CACHE_TYPE = "SimpleCache"

    FORCE_HTTPS = False

    APPLY_REDIRECTS = False
