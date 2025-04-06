import logging
from random import choice

from ...utils.decorator.decorators import retry
from .netease import client as netease_client
from .nexmo_sms import client as nexmo_client
from .twilio_client import client as twilio_client


logger = logging.getLogger(__name__)


class SmsSenderPool:
    def __init__(self):
        # 可以在中国用的服务商
        self.client_pool_china = [netease_client]
        # 可以在国外使用的服务商
        self.client_pool_intl = [twilio_client, nexmo_client]

    @retry(times=2)
    def send_code_by_country(self, mobile, country_code):
        if country_code in ("+86", "86"):
            client = choice(self.client_pool_china)
            response = client.send_code_with_country(mobile, country_code)
            result = self._format_response(client.APP_NAME, response)
        else:
            client = choice(self.client_pool_intl)
            response = client.send_code_with_country(mobile, country_code)
            result = self._format_response(client.APP_NAME, response)
        # 当发送失败时，使用Twilo发送
        if result.get("status_code") != 200:
            logger.error(
                "try twilio, current_client: {}, mobile: {}, country_code: {}, result: {}, response: {}".format(
                    client.APP_NAME, mobile, country_code, result, response
                )
            )
            client = twilio_client
            response = client.send_code_with_country(mobile, country_code)
            result = self._format_response(client.APP_NAME, response)
        logger.info(
            "client: {}, mobile: {}, country_code: {}, result: {}, response: {}".format(
                client.APP_NAME, mobile, country_code, result, response
            )
        )
        print(
            "mobile: {}, country_code: {}, result: {}, response: {}".format(
                mobile, country_code, result, response
            )
        )
        return result

    @staticmethod
    def _format_response(app_name, response):
        new_response = dict()
        if app_name == "Nexmo":
            status = response[0]["messages"][0]["status"]
            new_response["status_code"] = 200 if status == "0" else status
            new_response["verify_code"] = response[1]
            new_response["raw_data"] = response

        elif app_name == "Netease":
            new_response["status_code"] = response[0].get("code")
            new_response["verify_code"] = response[1]
            new_response["raw_data"] = response

        elif app_name == "Twilio":
            status = response[0].get("status_code")
            new_response["status_code"] = status
            new_response["verify_code"] = response[1]
            new_response["raw_data"] = response
        else:
            new_response["status_code"] = 400
        return new_response
