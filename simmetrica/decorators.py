__author__ = 'peter'

from settings import CACHE_TIMEOUT, CACHE_KEY
from functools import wraps
from google.appengine.api import memcache

def cached(timeout=CACHE_TIMEOUT, key=CACHE_KEY):
    def decorator(func):
        @wraps(func)
        def decorated_function(self, sql):
            cache_key=key.format(hash(sql))
            rv=memcache.get(cache_key)
            if rv:
                return rv
            rv=func(self, sql)
            if rv:
                memcache.set(cache_key, rv, time=timeout)
            return rv
        return decorated_function
    return decorator
