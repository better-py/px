import logging

from django.core.cache import caches as DjangoCaches


logger = logging.getLogger(__name__)


class BaseRedisCacheHandler:
    """

    :ref:
        - django_redis.cache.RedisCache()
        - django_redis.client.default.DefaultClient()#set()


    """

    CACHE_BACKEND = DjangoCaches["default"]

    def __init__(self, cache: DjangoCaches = None):
        self.client = cache or self.CACHE_BACKEND

    def get(self, key):
        return self.client.get(key)

    def set(self, key, value, timeout=None):
        return self.client.set(key, value, timeout)

    def update(self, key, value: dict, timeout=None):
        """部分更新 value 内容

        :param key:
        :param value: 字典类型
        :param timeout:
        :return:
        """
        raw = self.get(key) or {}
        if not isinstance(value, dict):
            return None
        raw.update(value)
        return self.set(key, raw, timeout)

    def delete(self):
        pass


class ServerCache(BaseRedisCacheHandler):
    """服务自身 cache 服务"""

    CACHE_BACKEND = DjangoCaches["default"]
