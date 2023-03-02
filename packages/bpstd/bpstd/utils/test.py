# -*- coding: utf-8 -*-
# @CreateDatetime    :2018/3/14:18:25
# @Author            :Helen
# @Product           :exchange-server
# @Description       :
import django.core.cache
import redis
from django.conf import settings

from maneki.apps.common.utils.cache import Cache
# -*- encoding:utf-8 -*-

redis_url = settings.CACHES["engine_proxy"]


def test_cache():

    msg = {
        "user_id": '11',
        "token":
            'token',
        "account": 'email',
        "engine_token": 'token',
    }

    # django.core.cache.cache.set(1,msg)
    Cache(db='engine_proxy')._put(12, msg)


class RedisCacheBase(object):
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    @property
    def client(self):
        pool = redis.ConnectionPool(
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
        )
        conn = redis.StrictRedis(connection_pool=pool)
        return conn


class RedisCache(RedisCacheBase):
    pass


def test_c():
    r = RedisCache()
    rc = r.client
    msg = {
        "user_id": '11',
        "token":
            'token',
        "account": 'email',
        "engine_token": 'token',
    }
    value = str(msg).encode('utf-8')

    rc.set('zzz', value)
