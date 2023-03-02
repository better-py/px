import logging

import requests

logger = logging.getLogger(__name__)


class SendCloudV2(object):
    """

    ref: http://sendcloud.sohu.com/doc/email_v2/

    """
    API_USER = "btccexchange"  # test user
    API_KEY = "S96GtISlbDANTjrW"
    #
    # API_DOMAIN = "btcchina.org"
    # TODO API域名修改为btcc.com
    API_DOMAIN = "btc250.com"
    #
    API_PREFIX = "http://api.sendcloud.net/apiv2"

    def __init__(self, api_user=None, api_key=None, api_prefix=None):
        self.api_user = api_user or self.API_USER
        self.api_key = api_key or self.API_KEY
        self.api_prefix = api_prefix or self.API_PREFIX
        #
        self.params_v2 = {
            "apiUser": self.api_user,
            "apiKey": self.api_key,
        }
        #
        self.params_v1 = {
            "api_user": self.api_user,
            "api_key": self.api_key,
        }

    def _do_get(self, url, payload: dict):
        payload.update(self.params_v2)
        r = requests.get(url, params=payload)
        print(r.url)
        result = r.json()
        for k, v in result.items():
            print("\t{}: {}".format(k, v))
        return result

    def _do_post(self, url, payload: dict):
        payload.update(self.params_v2)
        r = requests.post(url, data=payload)
        print(r.url)
        result = r.json()
        for k, v in result.items():
            print("\t{}: {}".format(k, v))
        return result.get("result")

    def send_email(self, payload: dict):
        """
        :ref: http://sendcloud.sohu.com/doc/email_v2/send_email/
        :param payload:
        :return:
        """
        url = self.api_prefix + "/mail/send"
        return self._do_post(url, payload)

    def send_template_email(self, payload: dict):
        url = self.api_prefix + "/mail/sendtemplate"
        return self._do_post(url, payload)

    def template_list(self):
        url = self.api_prefix + "/template/list"
        return self._do_get(url, self.params_v2)


client = SendCloudV2(api_user='btccexchange', api_key='S96GtISlbDANTjrW')
