import logging

from django.utils import timezone


logger = logging.getLogger(__name__)


def format_orm_fields(func):
    """装饰器: 格式化 ORM 传参

    :param func:
    :return:
    """

    def wrapper(*args, **kwargs):
        logger.warning("func: {}, raw kwargs: {}".format(func.__name__, kwargs))
        for k, v in kwargs.items():
            if v is None:
                kwargs.pop(k)
        logger.warning("func: {}, fmt kwargs: {}".format(func.__name__, kwargs))

        result = func(*args, **kwargs)
        return result

    return wrapper


class BaseService:
    MODEL = None
    CACHE = None

    def __init__(self, model: object = None, cache=None):
        self._model = model or self.MODEL
        #
        self._objects = self._model.objects
        self._filter = self._model.objects.filter
        self._create = self._model.objects.create
        self._update = self._model.objects.update
        #
        self._cache = cache or self.CACHE

    @staticmethod
    def fmt_kv(kv: dict):
        """过滤掉值为None的传参

        - 配合装饰器使用, 在多个 kv 传参时, 使用

        :param kv: type=dict
        :return:
        """
        logger.debug("ORM kv(raw): {}".format(kv))
        for k, v in kv.items():
            if v is None:
                kv.pop(k)
        logger.debug("ORM kv(fmt): {}".format(kv))
        return kv

    def filter_one(self, query_fields: dict):
        """单条查询

        :param query_fields: type=dict
        :return:
        """
        query_fields = self.fmt_kv(query_fields)

        one = self._filter(**query_fields).first()
        return bool(one), one

    def filter_many(self, query_fields: dict):
        """批量查询

        :param query_fields: type=dict
        :return:
        """
        query_fields = self.fmt_kv(query_fields)

        many = self._filter(**query_fields).all()
        return bool(many), many

    def create_one(self, query_fields: dict, create_fields: dict):
        """单条创建

        :param query_fields: type=dict
        :param create_fields: type=dict
        :return:
        """
        query_fields = self.fmt_kv(query_fields)
        create_fields = self.fmt_kv(create_fields)

        is_ok, one = self.update_one(
            query_fields=query_fields, update_fields=create_fields
        )
        if not is_ok:
            one = self._create(**create_fields)
        return True, one

    def update_one(self, query_fields: dict, update_fields: dict):
        """单条更新

        :param query_fields: type=dict
        :param update_fields: type=dict
        :return:
        """
        # fix: .update() 只能在 queryset 上执行, 不可用是单个obj.
        is_ok, many = self.update_many(
            query_fields=query_fields, update_fields=update_fields
        )
        one = many[0] if many else None
        return is_ok, one

    def update_many(self, query_fields: dict, update_fields: dict):
        """批量更新

        :param query_fields:
        :param update_fields:
        :return:
        """
        query_fields = self.fmt_kv(query_fields)
        update_fields = self.fmt_kv(update_fields)

        is_ok, many = self.filter_many(query_fields=query_fields)
        if not many:
            return False, None

        logger.warning("update count={}".format(many.count()))
        many.update(**update_fields)
        return True, many

    def soft_delete_one(self, query_fields: dict):
        """单条软删除

        :param query_fields:
        :return:
        """
        query_fields = self.fmt_kv(query_fields)

        is_ok, one = self.filter_one(query_fields=query_fields)
        if not one:
            return False, None
        one.soft_delete()
        return True, one

    def soft_delete_many(self, query_fields: dict):
        """批量软删除

        :param query_fields:
        :return:
        """
        query_fields = self.fmt_kv(query_fields)
        delete_fields = {
            "is_deleted": True,
            "deleted_at": timezone.now(),
        }
        return self.update_many(query_fields=query_fields, update_fields=delete_fields)

    @staticmethod
    def fmt_cache_key(key: str, prefix_fields: list):
        """格式化 key

        :param key: m
        :param prefix_fields: [a,b,c,d]
        :return: a:b:c:d:m
        """
        if not prefix_fields:
            return key
        prefix_fields.append(key)
        key = ":".join(prefix_fields)
        return key

    def cache_set(
        self, key: str, key_prefix_fields: list, value: dict, expired: int = None
    ):
        """单条cache设置

        : ref:
            - http://django-redis-chs.readthedocs.io/zh_CN/latest/#id14

        :param key:
        :param key_prefix_fields: [a, b, c, d]
        :param value: type=dict
        :param expired: [timeout=0 立即过期, timeout=None 永不过期]
        :return:
        """
        key = self.fmt_cache_key(key=key, prefix_fields=key_prefix_fields)
        return self._cache.set(key, value, expired)

    def cache_get(self, key: str, key_prefix_fields: list):
        """单条cache查询

        :param key:
        :param key_prefix_fields:
        :return:
        """
        key = self.fmt_cache_key(key=key, prefix_fields=key_prefix_fields)
        logger.debug("cache ttl: key={}, alive={}".format(key, self._cache.ttl(key)))
        return self._cache.get(key)

    def cache_delete(self, key: str, key_prefix_fields: list):
        """
        : ref:
            - timeout=0 立即过期
            - http://django-redis-chs.readthedocs.io/zh_CN/latest/#id14

        :param key:
        :param key_prefix_fields:
        :return:
        """
        key = self.fmt_cache_key(key=key, prefix_fields=key_prefix_fields)
        return self._cache.set(key, "delete", timeout=0)

    def cache_lock(self, key: str):
        """
        : ref:
            - http://django-redis-chs.readthedocs.io/zh_CN/latest/#locks

        :param key:
        :return:
        """
        with self._cache.lock(key):
            # 装饰器, 分布式锁机制
            # do_some_thing()
            pass
