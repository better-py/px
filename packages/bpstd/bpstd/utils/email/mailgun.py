import requests
import logging

logger = logging.getLogger(__name__)


class MailGun(object):
    """

    ref: http://sendcloud.sohu.com/doc/email_v2/

    """
    API_USER = "default_api_user"  # test user
    API_KEY = "key-98fa5d0f403bed6e8a1576a78f085b2e"
    #
    API_DOMAIN = "sandbox59ada4e04f1048c7829d6b1023583870.mailgun.org"
    #
    API_PREFIX = "https://api.mailgun.net/v3/"

    def __init__(self, api_key=None, domain=None):
        self.api_key = api_key or self.API_KEY
        self.api_domain = domain or self.API_DOMAIN
        self.api_prefix = self.API_PREFIX

    def send_email(self, payload: dict):
        """
        :ref: http://sendcloud.sohu.com/doc/email_v2/send_email/
        :param payload:
        :return:
        """

        url = self.api_prefix + self.API_DOMAIN+"/messages"

        result = requests.post(url,
                               auth=("api", self.api_key),
                               data=payload)
        logger.info("send email from mail gun, url:{}\n data: {}\n result:{}".format(url, payload, result.content))

        return result


