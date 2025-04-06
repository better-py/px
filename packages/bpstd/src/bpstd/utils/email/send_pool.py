import logging
from random import choice

from ...utils.decorator.decorators import retry
from .mail_gun import client as mail_client
from .sendcloud import client as send_client
from .smtp2go import client as smtp_client


logger = logging.getLogger(__name__)


class EmailSenderPool:
    def __init__(self):
        # TODO 增加邮件服务商到发送池
        self.client_pool = [send_client, mail_client]

    def _random_send_client(self):
        return choice(self.client_pool)

    @retry(times=3)
    def send_template_mail(self, payload):
        logger.info("send_email, payload: {}".format(payload))
        client = send_client
        r = client.send_template_email(payload=payload)
        if not r:
            client = mail_client
            r = client.send_template_email(payload=payload)
        return r

    def send_template_sm_mail(self, payload):
        client = smtp_client
        r = client.send_template_email(payload=payload)
        if not r:
            r = self.send_template_mail(payload=payload)
        return r
