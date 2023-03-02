# -*- coding: utf-8 -*-
import logging
import hashlib
import hmac
from collections import OrderedDict
from urllib import parse as url_parse

logger = logging.getLogger(__name__)


# 生成签名:
def generate_sign_sha512(payload: dict, secret_key: str):
    return _generate_signature(payload, secret_key, hashlib.sha512)


# 生成签名:
def generate_sign_sha256(payload: dict, secret_key: str):
    return _generate_signature(payload, secret_key, hashlib.sha256)


# 生成签名:
def _generate_signature(payload: dict, secret_key: str, sign_type: str):
    """ 生成签名

    :param payload: 待签名数据, type=dict
    :param secret_key: 私钥
    :param sign_type: 签名类型: [hashlib.sha512, hashlib.sha256]
    :return:
    """
    enc_payload = format_payload(payload)

    signed = hmac.new(
        bytes(secret_key, encoding='utf8'),
        bytes(enc_payload, encoding='utf8'),
        sign_type,
    ).hexdigest()
    return signed


# 签名校验:
def validate_sign_sha512(payload: dict, secret_key: str, input_sign: str):
    signature = generate_sign_sha512(payload, secret_key)
    logger.warning("input_sign={}, sign={}".format(input_sign, signature))
    return signature == input_sign


# 签名校验:
def validate_sign_sha256(payload: dict, secret_key: str, input_sign: str):
    signature = generate_sign_sha256(payload, secret_key)
    logger.warning("input_sign={}, sign={}".format(input_sign, signature))
    return signature == input_sign


# 格式化字段:
def format_payload(payload: dict, sign_field_name: str = "signature"):
    """格式化 k-v 参数对

    :param payload:
    :param sign_field_name: filter sign field
    :return:
    """
    payload = OrderedDict(payload)
    # fix: duplicate sign field
    if payload.get(sign_field_name):
        payload.pop(sign_field_name)

    logger.warning("sorted payload={}".format(payload))
    return url_parse.urlencode(payload)


# 格式化:
def format_url(base_url: str, url_suffix: str, params=""):
    """格式化 URL+参数

    :param base_url:
    :param url_suffix:
    :param params:
    :return:
    """
    url = base_url + url_suffix
    url = url + "/{}".format(params) if params else url
    return url


if __name__ == '__main__':
    for func in (generate_sign_sha512, generate_sign_sha256):
        result = func({"name": "jim", "msg": "hello"}, "hello")
        print(result)
