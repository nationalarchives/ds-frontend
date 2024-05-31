import os

from app.lib.util import strtobool


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY", "")
    DEBUG = strtobool(os.getenv("DEBUG", "False"))
    WAGTAIL_API_URL = os.environ.get("WAGTAIL_API_URL", "").rstrip("/")
    SEARCH_API_URL = os.environ.get("SEARCH_API_URL", "").rstrip("/")
    DOMAIN = os.environ.get("DOMAIN", "")
    MEDIA_DOMAIN = os.environ.get("MEDIA_DOMAIN", "")
    CACHE = {"CACHE_TYPE": "SimpleCache"}
    FORCE_HTTPS = False
    DOMAIN = os.environ.get("DOMAIN", "")
    WAGTAIL_MEDIA_URL = os.environ.get("WAGTAIL_MEDIA_URL", "").rstrip("/")
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


class ProductionConfig(Config):
    ENVIRONMENT = "production"
    CACHE = {
        "CACHE_TYPE": "FileSystemCache",
        "CACHE_DEFAULT_TIMEOUT": int(
            os.environ.get("CACHE_DEFAULT_TIMEOUT", 300)
        ),
        "CACHE_IGNORE_ERRORS": True,
        "CACHE_DIR": os.environ.get("CACHE_DIR", "/tmp"),
    }
    FORCE_HTTPS = True


class DevelopmentConfig(Config):
    ENVIRONMENT = "develop"
    DEBUG = True
    CACHE = {
        "CACHE_TYPE": "FileSystemCache",
        "CACHE_DEFAULT_TIMEOUT": int(
            os.environ.get("CACHE_DEFAULT_TIMEOUT", 1)
        ),
        "CACHE_IGNORE_ERRORS": True,
        "CACHE_DIR": os.environ.get("CACHE_DIR", "/tmp"),
    }


class TestingConfig(Config):
    ENVIRONMENT = "test"
    SECRET_KEY = ""
    DEBUG = True
    WAGTAIL_API_URL = "test"
    SEARCH_API_URL = ""
    DOMAIN = ""
    MEDIA_DOMAIN = ""
