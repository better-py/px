# -*- coding: utf-8 -*-
from maneki.apps.common.utils import date


def format_timestamp(timestamp, timedelta_day=30):
    if timestamp:
        timestamp = date.unix_to_datetime(int(timestamp[0:10]), "%Y-%m-%d %H:%M:%S")
    else:
        timestamp = date.utc_now_str(timedelta_day=timedelta_day)
    return timestamp
