from config import cache_config
from flask_caching import Cache

cache = Cache(config=cache_config)
