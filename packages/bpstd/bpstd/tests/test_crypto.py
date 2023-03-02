# -*- coding: utf-8 -*-
from django.test import TestCase

from ..utils import generate_nonce_8bit
from ..utils import generate_secret_key_64bit
from ..utils import generate_secret_key_v3
from ..utils import generate_sign_sha512
from ..utils import generate_timestamp_13bit
from ..utils import get_zone_time
from ..utils import validate_sign_sha512


def test_utils():
    key1 = generate_secret_key_v3()
    print(key1)


def test_generate_timestamp():
    t = get_zone_time()
    print(t)


# 签名生成+验证:
def test_sign():
    secret_key = generate_secret_key_64bit()
    payload = {
        "coin_type": "BTC",
        "amount": "0.1234",
        "nonce": generate_nonce_8bit(),
        "timestamp": generate_timestamp_13bit(),
    }

    sign = generate_sign_sha512(payload, secret_key)
    status = validate_sign_sha512(payload, secret_key, sign)

    for item in (secret_key, payload, sign, status):
        print("\t", item)
