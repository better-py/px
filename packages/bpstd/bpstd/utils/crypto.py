# -*- coding: utf-8 -*-
import binascii
import hashlib
import os
import secrets
import string

from django.utils.crypto import get_random_string

"""
secrets 包:
    - 只存在 python3.6 中,
    - 低版本, 可以移植该lib代码, 很简短

ref:
    - sentry.models.projectkey.ProjectKey()
    - sentry.utils.otp.generate_secret_key()


"""


def generate_secret_key_32bit():
    """ 生成32位随机数: (数字+大小写字母+安全符号)

        示例:
            - 2xIh1zpD71ZGiWpHYlG9OcoXtDmaeQinq_lae4z_H7r4etaKkl9Kvc8bKAxtTYqX
            - 6Y3RKdcdpfz9mogLzvSwpzD3eZvV6F1S01hI5Fio9FSYUliT03nrln1ENNg3xj3O
    :return:
    """
    return secrets.token_urlsafe(24)


def generate_secret_key_64bit():
    """ 生成64位随机数: (数字+大小写字母+安全符号)

        示例:
            - 2xIh1zpD71ZGiWpHYlG9OcoXtDmaeQinq_lae4z_H7r4etaKkl9Kvc8bKAxtTYqX
            - 6Y3RKdcdpfz9mogLzvSwpzD3eZvV6F1S01hI5Fio9FSYUliT03nrln1ENNg3xj3O
    :return:
    """
    return secrets.token_urlsafe(48)


def generate_secret_key_v2(length=64):
    """ 生成64位随机数: (数字+字母大小写)

        - string.ascii_letters: 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        - string.punctuation:  '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

    :return:
    """
    alphabet = string.ascii_letters + string.digits

    key = ''.join(
        secrets.choice(alphabet)
        for _ in range(length)
    )
    return key


def generate_secret_key_v3(length=64):
    """
        示例:
            - XWocpPkb1iL03fi5rP1xgZn0YdzOsGHQDZuJ49E7YREFfyi0zRvaMufaf7G0zba4
            - d0IDc7iEBRJreXbxzuFIbcDaps0NkaVAjaVVx4AkdPubcorDL7sdnSOkXGCeTBjv
    :param length:
    :return:
    """
    return get_random_string(length)


def generate_secret_key_v4(length=32):
    """生成64位随机字符串: hex数字

    :param length: =32, 返回长度为64
    :return:
    """
    return binascii.hexlify(os.urandom(length)).decode()


def generate_nonce_8bit(length=6):
    """生成随机字符串, 防止重放攻击

    :param length: =6, 返回长度为 8
    :return: ['1AieFdS1', 't1YCflcD']
    """
    return secrets.token_urlsafe(length)


def generate_nonce_8bit_digits(length=8, allowed_chars="0123456789"):
    """生成8位随机数字

    :param length:
    :param allowed_chars:
    :return:
    """
    return get_random_string(length, allowed_chars)


def generate_key_hash(raw_key: str):
    """ 生成 md5 hash值

    :param raw_key:
    :return: md5: hex, length=32
    """
    return hashlib.md5(raw_key.encode()).hexdigest()
