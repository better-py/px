import logging
from redis import StrictRedis
from django.conf import settings

logger = logging.getLogger(__name__)


def redis_client(redis_url, db: int):
    """根据URL初始化redis client

    :ref: https://github.com/andymccurdy/redis-py
    :param redis_url:
    :param db:
    :return: 返回连接池对象
    """
    logger.debug("redis client: {}, {}".format(redis_url, db))
    return StrictRedis.from_url(
        url=redis_url,
        db=db,
        decode_responses=True,
    )


def redis_client2(host: str = None, port: int = None, db: int = None):
    return StrictRedis(
        host=host, port=port, db=db,
        decode_responses=True,
    )


class RedisClient(object):

    def __init__(self, host=None, port=None, db=None, decode_responses=False, **kwargs):
        if kwargs.get('url', False):
            url = kwargs.get('url')
            self.client = StrictRedis.from_url(url=url, db=db, decode_responses=decode_responses)
        else:
            self.client = StrictRedis(host=host, port=port, db=db, decode_responses=decode_responses)


redis_sessions = {
    'UserInfo': RedisClient(url=settings.REDIS_LOCATION_USER_INFO).client,
    'Permission': RedisClient(url=settings.REDIS_LOCATION_USER_INFO).client,
    'BlackList': RedisClient(url=settings.REDIS_LOCATION_USER_BLACK_LIST).client,
    'TokenAuth': RedisClient(url=settings.REDIS_LOCATION_USER_INFO, decode_responses=True).client,

}

TOKEN_PREFIX = 'auth:token:'


def get_token_cache_key(key, prefix=TOKEN_PREFIX):
    return prefix + key
