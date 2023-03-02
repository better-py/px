# -*- coding: utf-8 -*-
import logging
import random
import time
import hashlib

import requests

from config.settings.env import NE_CAPTCHA_ID, NE_SECRET_ID, NE_SECRET_KEY

VERSION = "v2"
logger = logging.getLogger(__name__)


class NECaptchaVerifier(object):
    REQ_VALIDATE = "NECaptchaValidate"
    API_URL = "http://c.dun.163yun.com/api/v2/verify"
    CAPTCHA_ID = NE_CAPTCHA_ID
    SECRET_ID = NE_SECRET_ID
    SECRET_KEY = NE_SECRET_KEY

    def __init__(self, captcha_id=None, secret_id=None, secret_key=None):
        self.captcha_id = captcha_id or self.CAPTCHA_ID
        self.secret_id = secret_id or self.SECRET_ID
        self.secret_key = secret_key or self.SECRET_KEY

    def _do_post(self, payload):
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
        }
        response = requests.post(self.API_URL, data=payload, timeout=5, headers=headers)
        return response

    def verify(self, validate, user="{'user':123345}"):
        params = dict()
        params["captchaId"] = self.captcha_id
        params["validate"] = validate
        params["user"] = user
        params["secretId"] = self.secret_id
        params["version"] = VERSION
        params["timestamp"] = int(time.time() * 1000)
        params["nonce"] = int(random.random() * 100000000)
        params["signature"] = self.sign(params)

        print("ne_captcha debug: {}".format(params))
        logger.info("ne_captcha debug: {}".format(params))

        try:
            response = self._do_post(params)
            response_data = response.json()
            logger.info("ne_captcha_response: {}".format(response_data))
            return response_data['result'] if 'result' in response_data else False
        except Exception as e:
            print("ne_captcha API fail: {}".format(e))
            logger.error("ne_captcha API fail: {}".format(e))
            return False

    def sign(self, params=None):
        buff = ""
        for k in sorted(params.keys()):
            buff += str(k) + str(params[k])
        buff += self.secret_key
        return hashlib.md5(buff.encode('utf8')).hexdigest()
