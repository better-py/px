# -*- coding: utf-8 -*-
import json
import logging
import requests
from ..utils.email import template

logger = logging.getLogger(__name__)


class SMTP2GO(object):
    """
    Request Example https://api.smtp2go.com/v3/email/send
    ----------------------------------------------------------
    Response Example
    {
      "request_id": "aa253464-0bd0-467a-b24b-6159dcd7be60",
      "data":
      {
        "succeeded": 1,
        "failed": 0,
        "failures": [],
        "email_id": "1er8bV-6Tw0Mi-7h"
      }
    }
    """
    API_KEY = "api-9C01F01E5D8911E8A2E5F23C91C88F4E"
    API_DOMAIN = "btcc.com"
    API_PREFIX = "https://api.smtp2go.com/v3/"

    #
    def __init__(self, api_key=None, api_prefix=None, api_domain=None):
        self.api_key = api_key or self.API_KEY
        self.api_prefix = api_prefix or self.API_PREFIX
        self.api_domain = api_domain or self.API_DOMAIN
        self.auth_params = {
            "api_key": self.api_key
        }

    def _do_post(self, url, payload: dict):
        payload.update(self.auth_params)
        r = requests.post(url, json=payload)
        print(r.url)
        result = r.json()
        for k, v in result.items():
            print("\t{}: {}".format(k, v))
        return result.get("data").get('succeeded')

    def send_template_email(self, payload: dict):
        """
        格式化发送信息
        :param payload:
        email_content = {
            "from": email_from,
            "to": email,
            "fromName": email_from,
            "subject": email_subject,
            # 服务商配置邮件模板ID
            "templateInvokeName": email_template,
            "xsmtpapi": json.dumps(xsmtpapi),
        }
        :return:
        """
        template_id = payload.get('templateInvokeName')
        data = json.loads(payload.get('xsmtpapi'))
        # 传入模板的字符
        template_data = {
            'verify_code': data.get('sub').get('%url%')[0],
            'user_name': data.get('sub').get('%name%')[0]
        }
        new_payload = {
            'user_name': template_data.get('user_name'),
            'user_email': payload.get('to'),
            'email_from': payload.get('fromName'),
            'subject': payload.get('subject'),
            'template_id': template_id,
            'template_data': template_data,
            'api_domain': self.api_domain
        }

        return self.send_mail(**new_payload)

    def send_mail(self, user_name, user_email, email_from, subject, template_id, template_data: dict, api_domain):
        """
        发送邮件
        :ref: https://apidoc.smtp2go.com/documentation/#/POST%20/email/send
        {
            "api_key": "api-40246460336B11E6AA53F23C91285F72",
            "to": ["Test Person <test@example.com>"],
            "sender": "Test Persons Friend <test2@example.com>",
            "subject": "Hello Test Person",
            "text_body": "You're my favorite test person ever",
            "html_body": "<h1>You're my favorite test person ever</h1>",
            "custom_headers": [
              {
                "header": "Reply-To",
                "value": "Actual Person <test3@example.com>"
              }
            ]
        }
        :return:
        """
        url = self.api_prefix + "/email/send"
        http_data = {
            "to": ["{} <{}>".format(user_name, user_email)],
            "sender": "{} <no_reply@{}>".format(email_from, api_domain),
            "subject": subject,
            "html_body": self._get_html(template_id, template_data),
            "custom_headers": []
        }
        return self._do_post(url, http_data)

    def _get_html(self, template_id, data: dict):
        return self._template(**data).get(template_id)

    @staticmethod
    def _template(verify_code='', user_name=''):
        return {
            "btcc_mail": template.btcc_mail.format(verify_code),
            "trade_verify": template.btcc_mail.format(verify_code),
            "kyc_l2": template.kyc_l2.format(user_name),
            "kyc_l3": template.kyc_l3.format(user_name),
            "kyc_l4": template.kyc_l4.format(user_name),
            "kyc_no": template.kyc_no.format(user_name)
        }


client = SMTP2GO(api_key='api-DB5BB0305F3A11E88B11F23C91C88F4E')
