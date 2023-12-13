import os
from distutils.util import strtobool


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DEBUG = strtobool(os.getenv("DEBUG", "False"))


config = {
    "WAGTAIL_API_URL": os.environ.get("WAGTAIL_API_URL"),
    "WAGTAIL_MEDIA_URL": os.environ.get("WAGTAIL_MEDIA_URL"),
}

cache_config = {
    "CACHE_TYPE": "FileSystemCache",
    "CACHE_DEFAULT_TIMEOUT": int(os.environ.get("CACHE_DEFAULT_TIMEOUT", 300)),
    "CACHE_IGNORE_ERRORS": True,
    "CACHE_DIR": "/tmp",
}
