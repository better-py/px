from functools import wraps

from django.db import connections


def verify_db_connections(f):
    @wraps(f)
    def _wrapper(*args, **kwargs):
        for conn in connections.all():
            conn.close_if_unusable_or_obsolete()  # django db connection is easy to lost !!!
        return f(*args, **kwargs)

    return _wrapper
