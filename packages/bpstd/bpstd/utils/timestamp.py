import time
from datetime import datetime

from django.utils import timezone


def generate_timestamp_13bit():
    """13 位整数的毫秒时间戳
        - python 默认是10位, java默认是13位(毫秒级)
        - Unix 时间戳根据精度的不同，有 10 位（秒级），13 位（毫秒级），16 位（微妙级）和 19 位（纳秒级）
    :return:
    """
    ts = int(round(time.time() * 1000))
    # ts = time.time() * 1000
    # int(datetime.now().timestamp()) * 1000
    return ts


def generate_timestamp_10bit():
    """10 位整数的时间戳

    :return:
    """
    return int(time.time())


# 获取当前时间(年月日):
def get_current_date():
    return datetime.today().strftime("%Y%m%d")


def get_zone_time():
    return timezone.now()
