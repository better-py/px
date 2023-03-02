# -*- coding: utf-8 -*-
import logging
import requests
from ...utils.email.smtp2go import SMTP2GO

logger = logging.getLogger(__name__)


class MailGun(SMTP2GO):

    API_KEY = "key-23defeb1513049291b8f5e327b2aba32"
    API_DOMAIN = "btc250.com"
    API_PREFIX = "https://api.mailgun.net/v3/"

    def __init__(self, api_key=None, api_prefix=None, api_domain=None):
        super(MailGun, self).__init__(api_key, api_prefix, api_domain)
        self.auth_params = ('api', self.api_key)

    # def send_complex_message():
    #     return requests.post(
    #         "https://api.mailgun.net/v3/YOUR_DOMAIN_NAME/messages",
    #         auth=("api", "YOUR_API_KEY"),
    #         files=[("attachment", ("test.jpg", open("files/test.jpg", "rb").read())),
    #                ("attachment", ("test.txt", open("files/test.txt", "rb").read()))],
    #         data={"from": "Excited User <YOU@YOUR_DOMAIN_NAME>",
    #               "to": "foo@example.com",
    #               "cc": "baz@example.com",
    #               "bcc": "bar@example.com",
    #               "subject": "Hello",
    #               "text": "Testing some Mailgun awesomness!",
    #               "html": "<html>HTML version of the body</html>"})

    def _do_post(self, url, payload: dict):
        r = requests.post(url, data=payload, auth=self.auth_params)
        print(r.url)
        result = r.json()
        for k, v in result.items():
            print("\t{}: {}".format(k, v))
        if r.status_code == 200:
            return True
        else:
            return False

    def send_template_email(self, payload: dict):
        return super(MailGun, self).send_template_email(payload)

    def send_mail(self, user_name, user_email, email_from, subject, template_id, template_data: dict, api_domain):
        url = self.api_prefix + self.api_domain + "/messages"
        http_data = {
            "from": "{} <no_reply@{}>".format(email_from, api_domain),
            "to": user_email,
            "subject": subject,
            "html": self._get_html(template_id, template_data)
        }
        return self._do_post(url, http_data)


client = MailGun(api_domain='btc250.com')
