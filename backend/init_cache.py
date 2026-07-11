from flask_caching import Cache

cache = Cache()

def setup_cache(app):
  app.config["CACHE_TYPE"] = "RedisCache"
  app.config["CACHE_REDIS_URL"] = "redis://localhost:6379/2"
  app.config["CACHE_DEFAULT_TIMEOUT"] = 300  # 5 minutes

  cache.init_app(app)