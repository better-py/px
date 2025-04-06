import logging
import time
from functools import wraps

from django.core.cache import caches as DjangoCaches


logger = logging.getLogger(__name__)


def verify_key(f):
    @wraps(f)
    def _wrapper(*args, **kwargs):
        # for conn in connections.all():
        #     conn.close_if_unusable_or_obsolete()
        return f(*args, **kwargs)

    return _wrapper


def accepts_args(type, vaild):
    def decorator(f):
        @wraps(f)
        def new_f(data, arg1=None):
            if isinstance(data, type) is False:
                raise NotImplementedError
            if type == dict:
                for key in vaild:
                    if data.get(key) == None:
                        raise NotImplementedError
                return f(data)
            elif type == list:
                for i in range(len(data)):
                    for key in vaild:
                        if data[i].get(key) == None:
                            raise NotImplementedError
                return f(data, arg1)

        return new_f

    return decorator


def retry(times=3, failed_wait=1, raise_exec=False):
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for count in range(times):
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    logger.error(
                        "execute fn:{}, expection:{}".format(func.__name__, repr(e))
                    )
                    time.sleep(failed_wait)
                    if count == (times - 1) and raise_exec:
                        raise e
                    continue

        return wrapper

    return inner


def cache_first_get_user_info(fn):
    """from cache get user_info first.
    if not got then kwargs is None.
    then got from fn by logic
    """
    client = DjangoCaches["default"]

    @wraps(fn)
    def inner(*args, **kwargs):
        request = args[0]
        key = request.user.user_id
        user_info = client.get(key)
        if user_info:
            kwargs.update(user_info=user_info)
        return fn(*args, **kwargs)

    return inner()


def omit_exception(fn):
    """
    Simple decorator that ignored all exception
    errors and ignores these if settings specify this.
    """

    @wraps(fn)
    def _decorator(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            logger.exception(repr(e))

    return _decorator
