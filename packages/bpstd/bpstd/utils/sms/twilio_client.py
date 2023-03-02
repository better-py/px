import logging

from twilio.rest import Client

from ...utils import generate_nonce_8bit_digits

logger = logging.getLogger(__name__)


class TwiLio(object):
    TWILIO_ACCOUNT_SID = 'ACd8de43d24ae9ca914a1ae4a54e90520e'
    TWILIO_AUTH_TOKEN = '359a0a37fab1e8ce57711ba0eb86b095'
    MOBILE_FROM = '+13312156760'

    APP_NAME = "Twilio"

    def __init__(self, account_sid=None, auth_token=None, mobile_from=None):
        self.account_sid = account_sid if account_sid else self.TWILIO_ACCOUNT_SID
        self.auth_token = auth_token if auth_token else self.TWILIO_AUTH_TOKEN
        self.mobile_from = mobile_from if mobile_from else self.MOBILE_FROM
        self.client = Client(self.account_sid, self.auth_token)

    def send_text(self, to, content, send_from=None):
        msg = self.client.messages.create(
            body=content,
            from_=send_from if send_from else self.mobile_from,
            to=to
        )
        logger.debug(msg.sid)
        print(msg)
        return msg

    def send_code_with_country(self, mobile: str, mobile_country_code):
        code = generate_nonce_8bit_digits(length=4)
        text = """[BTCC] confirmation code: {}
Valid for 30 minutes.
Please delete If you did not request this.
DO NOT reveal this code to anyone.""".format(code)
        mobile = mobile
        response = self.send_text(to=mobile, content=text)
        data = self._deal_with_response(response)
        return data, code

    def _deal_with_response(self, response):
        code = response.error_code if response.error_code else 200
        data = {
            'status_code': code,
            'body': response
        }
        return data


client = TwiLio()
