import os

from app.lib.util import strtobool


class Config(object):
    ENVIRONMENT = os.environ.get("ENVIRONMENT", "production")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DEBUG = strtobool(os.getenv("DEBUG", "False"))
    WAGTAIL_API_URL = os.environ.get("WAGTAIL_API_URL").rstrip("/")
    WAGTAIL_MEDIA_URL = os.environ.get("WAGTAIL_MEDIA_URL").rstrip("/")
    SEARCH_API_URL = os.environ.get("SEARCH_API_URL").rstrip("/")
    ROSETTA_API_URL = os.environ.get("ROSETTA_API_URL").rstrip("/")


cache_config = {
    "CACHE_TYPE": "FileSystemCache",
    "CACHE_DEFAULT_TIMEOUT": int(os.environ.get("CACHE_DEFAULT_TIMEOUT", 300)),
    "CACHE_IGNORE_ERRORS": True,
    "CACHE_DIR": os.environ.get("CACHE_DIR", "/tmp"),
}
