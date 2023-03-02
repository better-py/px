from nexmo import Client

from maneki.apps.common.utils.crypto import generate_nonce_8bit_digits


class Nexmo(object):
    NEXMO_API_KEY = "38915e36"
    NEXMO_API_SECRET = "KZCSZP3uPlXnY4w1"
    SENDER = "BTCC"

    CODE_TEMPLATE = "Your code: {} from BTCC"

    APP_NAME = "Nexmo"

    def __init__(self, key=None, secret=None):
        self.key = key if key else self.NEXMO_API_KEY
        self.secret = secret if secret else self.NEXMO_API_SECRET
        self.client = Client(key=self.key, secret=self.secret)

    def send_text(self, to, content):
        return self.client.send_message({
            'from': self.SENDER,
            'to': to,
            'text': content,
        })

    def send_code_with_country(self, mobile: str, mobile_country_code):
        code = generate_nonce_8bit_digits(length=4)
        text = """[BTCC] confirmation code: {}
Valid for 30 minutes.
Please delete If you did not request this.
DO NOT reveal this code to anyone.""".format(code)
        mobile = mobile
        return self.send_text(to=mobile, content=text), code


client = Nexmo()
