# -*- coding: utf-8 -*-
# @CreateDatetime    :2018/3/2:19:09
# @Author            :Helen
# @Product           :exchange-server
# @Description       :
import pytest

from ..utils.redis import Redis


def test_set_dict():
    msg = {
        "user_id": '20',
        "token": 'xxxxxx',
        "account": 'x20',
    }
    r = Redis(session_key='test')
    r.save(msg)


def test_get_dict():

    r = Redis(session_key='test')
    result = r.load()
    print(result)
