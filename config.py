import os

from app.lib.util import strtobool


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DEBUG = strtobool(os.getenv("DEBUG", "False"))
    WAGTAIL_API_URL = os.environ.get("WAGTAIL_API_URL")
    WAGTAIL_MEDIA_URL = os.environ.get("WAGTAIL_MEDIA_URL")
    EXPLORE_PAGE_ID_ENTRY = os.environ.get("EXPLORE_PAGE_ID_ENTRY")
    AUTHORS_PAGE_ID_ENTRY = os.environ.get("AUTHORS_PAGE_ID_ENTRY")


cache_config = {
    "CACHE_TYPE": "FileSystemCache",
    "CACHE_DEFAULT_TIMEOUT": int(os.environ.get("CACHE_DEFAULT_TIMEOUT", 300)),
    "CACHE_IGNORE_ERRORS": True,
    "CACHE_DIR": os.environ.get("CACHE_DIR", "/tmp"),
}
