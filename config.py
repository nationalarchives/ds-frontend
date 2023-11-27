import os
from distutils.util import strtobool


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DEBUG = strtobool(os.getenv("DEBUG", "False"))
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 300
