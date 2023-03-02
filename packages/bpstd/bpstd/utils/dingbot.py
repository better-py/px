import os
import logging
import json
import requests

from celery import shared_task
from maneki.apps.common.utils.decorator.decorators import retry
from django.conf import settings
logger = logging.getLogger(__name__)

# slack bot token:
API_TOKEN = os.getenv("DING_API_TOKEN", "f53830543de7613e07a61cac36e81b12d5b157453bf77c5763a7543fbbdd9cae")
BASE_URL = 'https://oapi.dingtalk.com/robot/send?access_token={}'

API_URL = 'https://oapi.dingtalk.com/robot/send?access_token={}'.format(API_TOKEN)


@retry(times=3)
def send_markdown_msg(text, api_url, title=''):
    header = {'Content-Type': 'application/json; charset=utf-8'}

    # data = dict(msgtype="text", text=dict(content=text))
    data = dict(msgtype="markdown", markdown=dict(title=title, text=text))

    json_data = json.dumps(data)
    logger.info(json_data)
    result = requests.post(api_url, headers=header, data=json_data)

    if not result:
        raise Exception('request post unfinished')

    if result.status_code != 200:
        raise Exception('request fail code is:{}'.format(result.status_code))

    return result.content


@shared_task
def async_send_ding_msg(msg, token, title):
    api_url = BASE_URL.format(token)
    if settings.DEBUG:
        api_url = BASE_URL.format("e9801fe6a198b3bb4ce0d646c1e3ebcff44a981886f6c36685b4c755401718bd")
        send_markdown_msg(msg, api_url, title)
    else:
        send_markdown_msg(msg, api_url, title)
