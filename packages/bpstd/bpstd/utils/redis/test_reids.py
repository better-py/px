import json

from django.test import TestCase
from ...utils.redis.r import redis_sessions


class TestRedis(TestCase):

    def test_redis_set(self):
        user_info = {
            "uid": "f6c6c961707349989d2b622fcb3e122f",
            "email": "trace_tristan@126.com",
            "mobile": "",
            "level": 1,
            "is_double_check": True,
            "deposit_code": "KLTC448L",
            "nickname": "",
            "role_id": 1
            }

        # set 时dumps,get 用 json.loads redis设置 decode_responses=False
        user_info = json.dumps(user_info)
        redis_sessions['UserInfo'].set('test', user_info)

    def test_redis_get(self):
        user_info = redis_sessions['UserInfo'].get('test')
        user_info = json.loads(user_info)
        print(user_info)
