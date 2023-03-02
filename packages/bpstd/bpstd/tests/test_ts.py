from datetime import datetime
import pytest


def get_zero_timestamp():
    """默认零值 = 1970-01-01 00:00:01

    :return:
    """
    zero = datetime.fromisoformat("1970-01-01 00:00:01")
    return zero.timestamp()


def is_zero_timestamp(ts: int):
    """默认零值 = 1970-01-01 00:00:01

    :param ts:
    :return:
    """
    return ts == get_zero_timestamp()


def test_datetime():
    t = datetime.now()
    ts = datetime.fromisoformat("1970-01-01 00:00:01").timestamp()
    print(f"zero: {get_zero_timestamp()}, assert: {ts}")
    assert ts == get_zero_timestamp()

    print(datetime.max.timestamp(), datetime.min)
    print(datetime.fromisoformat("1970-01-01 00:00:01").timestamp())
    print(t.timestamp())
