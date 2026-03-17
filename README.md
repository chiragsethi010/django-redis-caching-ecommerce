## 🔴 Django Redis Caching — E-Commerce Product API

A production-style Django project demonstrating how to integrate Redis 
caching into a real-world e-commerce product API without Django REST Framework.

This project shows exactly how a request is served from cache (Redis) or 
database (PostgreSQL/SQLite), with live X-Cache headers, hit/miss tracking, 
and automatic cache invalidation using Django signals.

- Product list API that caches all products in Redis
- Product detail API with per-product cache key (product:<pk>)
- X-Cache: HIT / MISS response header on every request
- Auto cache invalidation on product create, update, delete using Django signals
- /cache-stats/ endpoint showing total hits, misses, and hit ratio
- CacheDebugMiddleware that adds cache timing headers
- Django Admin override that also clears cache on save/delete

What You Learned:--

- How Redis works as an in-memory cache layer in Django
- Cache-aside pattern (check cache → miss → query DB → store → return)
- How to configure django-redis in settings.py with KEY_PREFIX, TIMEOUT, 
  IGNORE_EXCEPTIONS, and hiredis parser
- cache.get(), cache.set(), cache.delete(), cache.incr() from Django cache API
- How to build meaningful cache keys using f-strings (product:{pk})
- How to auto-invalidate cache using Django post_save and post_delete signals
- How to write custom Django middleware
- How to verify cache behavior using redis-cli (TTL, KEYS, GET)
- How to measure cache performance using hit ratio
- Difference between cache HIT and cache MISS in a real request lifecycle

  Tech Stack--
python  django  redis  django-redis  caching  
cache-aside  redis-cache  backend  web-development  
rest-api  cache-invalidation  middleware  django-signals
