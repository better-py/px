# -*- coding: utf-8 -*-
#
# fix issue:
#   - https://docs.djangoproject.com/en/2.0/topics/cache/#cache-key-transformation
#


def make_key(key, key_prefix, version):
    """ 覆盖django cache 的实现. 不拼接版本.
    :param key:
    :param key_prefix:
    :param version:
    :return:
    """
    return key
