import time

from django.test import TestCase

from .mailgun import MailGun


class TestSendPool(TestCase):
    def tsend_mail_gun(self):
        playload = {
            "from": "register@btcc.com",
            "to": "yuan.gu@hpe.com",
            # "template_invoke_name": "test_template",
            "fromname": "henry",
            "subject": "BTCC EMAIL Confirm",
            "text": "hello btcc. {}".format(time.time()),
        }

        r = MailGun().send_email(playload)
        self.assertEqual(r.status_code, 200)
