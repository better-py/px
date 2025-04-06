from unittest import TestCase

from ..utils.sms.netease import NeteaseSMS
from ..utils.sms.nexmo_sms import Nexmo
from ..utils.sms.send_pool import SmsSenderPool
from ..utils.sms.twilio_client import TwiLio


class NeteaseSMSTest(TestCase):
    def setUp(self):
        app_key = "cd4e09d1b951a4c4d0c3eb5fcf01c8c8"
        app_secret = "a24e8ba3c4ab"

        self.mobile = "17192188380"
        self.api = NeteaseSMS(app_key, app_secret)

    def test_send_code(self):
        """
            url: https://api.netease.im/sms/sendcode.action
            HTTP-header: {
                            'AppKey': 'cd4e09d1b951a4c4d0c3eb5fcf01c8c8',
                            'CurTime': '1522316895',
                            'Nonce': '7347fef81510499db055f377ff574272',
                            'CheckSum': 'f0dcc94fc1d287304140a4ee62efa11463e1ee53',
                            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
                            }
            HTTP-data: {'mobile': '17192188380'}
            status: 200
            result: b'{"code":200,"msg":"3","obj":"2185"}'

        :return:
        """
        result = self.api.send_code(self.mobile)
        print("send code:", result)

        query_id = result["msg"]
        sms_code = result["obj"]
        print("query id:", query_id)

        result = self.api.query_status(query_id)
        print("query status: ", result)

        result = self.api.verify_code(self.mobile, sms_code)
        print("verify code: ", result)

    def test_send_template(self):
        """发送模板类验证码

        :return:
        """
        # 验证码模板:
        tp_login_id = "3057103"  # 不支持
        tp_register_id = "3061023"  # 不支持
        tp_id = "3049132"  # 支持

        templdate_id = "3893012"
        code = self.api.random_code
        result = self.api.send_template(
            templdate_id,
            self.mobile,
        )


"""
# 发送验证码短信:
url: https://api.netease.im/sms/sendcode.action
HTTP-header: {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8', 'CurTime': '1488347303', 'CheckSum': 'daf9bf5bf2d68715c9c12d5612b370ff27623273', 'Nonce': '775dd54709e74a808202a318fbb453eb', 'AppKey': '9b2a9ade419055031a6e3fab8f89e4XX'}

HTTP-data: {'mobile': '13380789XXX'}
	status: 200
	result: b'{"code":200,"msg":"14","obj":"3367"}'


# 查询发送状态:
url: https://api.netease.im/sms/querystatus.action
HTTP-header: {'Nonce': '61e9df9723e54bbf9f14892915ee4406', 'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8', 'CurTime': '1488347349', 'AppKey': '9b2a9ade419055031a6e3fab8f89e4XX', 'CheckSum': 'e9d47dc5c3347d906de1dbe8f8261a93fe7da01d'}

HTTP-data: {'sendid': '14'}
	status: 200
	result: b'{"code":200,"obj":[{"updatetime":1488347319329,"status":1,"mobile":"+86-13380789XXX"}]}'


# 验证验证码是否正确:
url: https://api.netease.im/sms/verifycode.action
HTTP-header: {'Nonce': 'eb66cf06072647f5af66a8e7ef6dcba0', 'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8', 'CurTime': '1488347350', 'AppKey': '9b2a9ade419055031a6e3fab8f89e4XX', 'CheckSum': '205618d4dc2d152b6ba1b3a85dc855292991109f'}
HTTP-data: {'mobile': '13380789XXX', 'code': '3367'}
	status: 200
	result: b'{"code":200}'


###############################################

# 发送模板验证码:
		code:472451
url: https://api.netease.im/sms/sendtemplate.action
HTTP-header: {'CurTime': '1488347659', 'CheckSum': '371657b31fb74b94d91a155930f3b2f4d8ce0766', 'Nonce': '164d8355b7464bef93bfe31fefe927d7', 'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8', 'AppKey': '9b2a9ade419055031a6e3fab8f89e4XX'}
HTTP-data: {'mobiles': "['13380789XXX']", 'params': "['472451']", 'templateid': '3049132'}
	status: 200 	result: b'{"code":200,"msg":"sendid","obj":15}'


# 模板验证码, 状态校验:(支持查询状态)
url: https://api.netease.im/sms/querystatus.action
HTTP-header: {'CurTime': '1488347793', 'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8', 'AppKey': '9b2a9ade419055031a6e3fab8f89e4XX', 'CheckSum': 'a309b5ec0b978bc09ba4fd4de6487e5e3662231e', 'Nonce': '0a603bd67b434acab1b37ee14e9b7dc4'}
HTTP-data: {'sendid': '15'}
	status: 200 	result: b'{"code":200,"obj":[{"updatetime":1488347672407,"status":1,"mobile":"13380789XXX"}]}'

# 模板验证码, 正确性检查:
#   - 不支持模板检查:
#   - 413	验证失败(短信服务)
#
url: https://api.netease.im/sms/verifycode.action
HTTP-header: {'CurTime': '1488347794', 'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8', 'AppKey': '9b2a9ade419055031a6e3fab8f89e4XX', 'CheckSum': '981c8e6888676d67eaea0139e12890cb8984c3f4', 'Nonce': '87e511c76e1947008f684529ee3f02e7'}
HTTP-data: {'mobile': '13380789XXX', 'code': '472451'}
	status: 200 	result: b'{"code":413,"msg":"verify err","obj":1}'



"""


class TwilioTest(TestCase):
    def setUp(self):
        self.phone_num = "+8615827629220"
        self.code = "+86"

    def test_sms(self):
        s = TwiLio()
        response = s.send_code_with_country(self.phone_num, self.code)
        # error_code = response[0].error_code
        print(response)
        code = response[0].get("status_code")
        assert code == 200
        return response

    def test_pool(self):
        s = SmsSenderPool()
        result = s.send_code_by_country(self.phone_num, self.code)
        print(result)
        return result

    def test_netease(self):
        s = NeteaseSMS()
        result = s.send_code_with_country(self.phone_num, self.code)
        assert result[0].get("code") == 200
        print(result)

    def test_nexmo(self):
        s = Nexmo()
        result = s.send_code_with_country(self.phone_num, self.code)
        assert result[0].get("messages")[0].get("status") == "0"
        print(result)
