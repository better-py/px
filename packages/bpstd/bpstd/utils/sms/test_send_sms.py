from django.test import TestCase

from maneki.apps.common.utils.sms.nexmo_sms import Nexmo
from maneki.apps.common.utils.sms.send_pool import SmsSender


class TestSendNexmo(TestCase):

    def test_send_code(self):
        country_code = "86"
        mobile = "18838113104"
        result = Nexmo().send_code_with_country(mobile, country_code)
        print(result)


class TestSendPool(TestCase):

    def test_send_china(self):
        country_code = "86"
        mobile = "18838113104"
        SmsSender().send_code_by_country(mobile, country_code)
