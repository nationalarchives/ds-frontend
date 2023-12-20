import os

from app.lib.util import strtobool


class Config(object):
    ENVIRONMENT = os.environ.get("ENVIRONMENT", "production")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DEBUG = strtobool(os.getenv("DEBUG", "False"))
    WAGTAIL_API_URL = os.environ.get("WAGTAIL_API_URL")
    WAGTAIL_MEDIA_URL = os.environ.get("WAGTAIL_MEDIA_URL")


cache_config = {
    # "CACHE_TYPE": "FileSystemCache",
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": int(os.environ.get("CACHE_DEFAULT_TIMEOUT", 300)),
    "CACHE_IGNORE_ERRORS": True,
    "CACHE_DIR": os.environ.get("CACHE_DIR", "/tmp"),
}
