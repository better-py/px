#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import random
import time
import uuid

import requests

from ...utils import generate_nonce_8bit_digits

"""

# 参考文档:
http://dev.netease.im/docs?doc=server_sms

# 校验:
http://dev.netease.im/docs?doc=server&#接口概述

# 说明:
- 本模块, 有提供接口调用示例.
- 完备测试.
- 未对 网易接口返回值, 作数据提取.
- 部分接口的传入参数, 需要从其他接口提取.


"""


class NeteaseSMS(object):
    """ 网易云信短信验证码服务 API 接口:
    """
    APP_KEY = "cd4e09d1b951a4c4d0c3eb5fcf01c8c8"
    APP_SECRET = "a24e8ba3c4ab"

    # API前缀:
    API_PREFIX = "https://api.netease.im/sms/"

    APP_NAME = "Netease"

    def __init__(self, app_key=None, app_secret=None):
        self.app_key = app_key or self.APP_KEY
        self.app_secret = app_secret or self.APP_SECRET

        # 接口列表:
        self.api_urls = {
            "send": self.API_PREFIX + "sendcode.action",
            "verify": self.API_PREFIX + "verifycode.action",
            "send_template": self.API_PREFIX + "sendtemplate.action",
            "query_status": self.API_PREFIX + "querystatus.action",
        }

    @property
    def nonce(self):
        return uuid.uuid4().hex

    @property
    def current_time(self):
        return str(int(time.time()))

    def checksum(self, nonce, current_time):
        s = "{}{}{}".format(self.app_secret, nonce, current_time).encode(encoding="utf-8")
        return hashlib.sha1(s).hexdigest()

    @property
    def http_headers(self):
        """ 构造 HTTP 请求头

        :return:
        """
        nonce = self.nonce
        current_time = self.current_time
        checksum = self.checksum(nonce, current_time)

        return {
            "AppKey": self.app_key,
            "CurTime": current_time,
            "Nonce": nonce,
            "CheckSum": checksum,
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        }

    @property
    def random_code(self):
        """ 自定义生成6位验证码
        :return:
        """
        return str(random.randint(100000, 999999))

    @staticmethod
    def _post(url, payload, headers):
        r = requests.post(url, data=payload, headers=headers)

        print("url: {}\nHTTP-Header: {}\nHTTP-Body: {}".format(url, headers, payload))
        print("\tstatus: {} \tresult: {}".format(r.status_code, r.content))
        return r.json() if r.status_code == 200 else {}

    ##################################################
    #              API 接口
    #
    ##################################################

    def send_code(self, mobile: str):
        """ 调用网易短信验证码服务接口, 发送验证码到手机.
        :param mobile: 手机号
        :return: 返回调用结果
                - {'msg': '4', 'code': 200, 'obj': '4123'}
                - obj: 验证码内容
                - code: 状态码
                - msg: 对应 查询里的 send_id 参数
        """
        payload = {
            "mobile": str(mobile) if not mobile.startswith("+86") else str(mobile).lstrip("+86"),
        }
        return self._post(self.api_urls["send"], payload=payload, headers=self.http_headers)

    def send_code_with_country(self, mobile: str, mobile_country_code):
        code = generate_nonce_8bit_digits(length=4)
        mobile = mobile.replace('+86', '')
        return self.send_template(mobiles=mobile, params=[code, code], template_id='3893012'), code

    def send_template(self, template_id, mobiles, params=None):
        """ 发送模板短信
        :param template_id: 模板 ID, 目前测试发现: 只支持通知类模板, 不支持验证码模板.
        :param mobiles: 手机号列表
        :param params: 参数列表
        :return:
        """
        payload = {
            "mobiles": str([mobiles]) if not isinstance(mobiles, list) else mobiles,
        }

        if template_id:
            payload.update({"templateid": str(template_id)})

        if params:
            params = [params] if not isinstance(params, list) else params
            payload.update({"params": str(params)})

        return self._post(self.api_urls["send_template"], payload=payload, headers=self.http_headers)

    def verify_code(self, mobile, code):
        """验证码正确性检查:
            - 只支持常规的验证码检查, 不支持模板验证码检查.
        :param mobile: 手机号
        :param code: 验证码, 对应 send_code() 返回值的 obj 字段
        :return:
        """
        payload = {
            "mobile": str(mobile),
            "code": str(code),
        }
        return self._post(self.api_urls["verify"], payload=payload, headers=self.http_headers)

    def query_status(self, send_id):
        """验证码发送状态查询:
            - 支持常规验证码检查, 同时也支持模板验证码检查.
        :param send_id: 发送 ID, 对应 send_code() 返回值的 msg 字段
        :return:
        """
        payload = {
            "sendid": str(send_id),
        }
        return self._post(self.api_urls["query_status"], payload=payload, headers=self.http_headers)


# Todo: add key to settings
client = NeteaseSMS(app_key="cd4e09d1b951a4c4d0c3eb5fcf01c8c8", app_secret="a24e8ba3c4ab")
