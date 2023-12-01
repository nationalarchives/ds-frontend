from flask_caching import Cache

from config import cache_config

cache = Cache(config=cache_config)
