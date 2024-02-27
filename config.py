import os

from app.lib.util import strtobool


class Config(object):
    ENVIRONMENT = os.environ.get("ENVIRONMENT", "production")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DEBUG = strtobool(os.getenv("DEBUG", "False"))
    WAGTAIL_API_URL = os.environ.get("WAGTAIL_API_URL").rstrip("/")
    SEARCH_API_URL = os.environ.get("SEARCH_API_URL").rstrip("/")
    DOMAIN = os.environ.get("DOMAIN", "")


cache_config = {
    "CACHE_TYPE": "FileSystemCache",
    "CACHE_DEFAULT_TIMEOUT": int(os.environ.get("CACHE_DEFAULT_TIMEOUT", 300)),
    "CACHE_IGNORE_ERRORS": True,
    "CACHE_DIR": os.environ.get("CACHE_DIR", "/tmp"),
}

templates_config = {
    "DOMAIN": os.environ.get("DOMAIN", ""),
    "WAGTAIL_MEDIA_URL": os.environ.get("WAGTAIL_MEDIA_URL").rstrip("/"),
    "BASE_DISCOVERY_URL": os.environ.get(
        "BASE_DISCOVERY_URL",
        "https://discovery.nationalarchives.gov.uk",
    ).rstrip("/"),
    "SEARCH_DISCOVERY_URL": os.environ.get(
        "SEARCH_DISCOVERY_URL",
        (
            os.environ.get(
                "BASE_DISCOVERY_URL",
                "https://discovery.nationalarchives.gov.uk",
            ).rstrip("/")
            + "/results/r"
        ),
    ),
    "SEARCH_WEBSITE_URL": os.environ.get(
        "SEARCH_WEBSITE_URL",
        "https://www.nationalarchives.gov.uk/search/results",
    ),
    "ARCHIVE_RECORDS_URL": os.environ.get(
        "ARCHIVE_RECORDS_URL",
        "https://discovery.nationalarchives.gov.uk/browse/r/h/",
    ),
    "GA4_ID": os.environ.get("GA4_ID"),
}
