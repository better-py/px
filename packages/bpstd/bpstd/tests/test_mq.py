import datetime

import pytest
from django.conf import settings

from ..utils.mq.pika import BaseConsumer
from ..utils.mq.pika import BaseProducer


def test_mq_conf():
    mq_conf = settings.RABBITMQ_CONFIG_GROUP

    for k, v in mq_conf.items():

        print("\t{}:".format(k))
        if isinstance(v, dict):
            for kk, vv in v.items():
                if isinstance(vv, dict):
                    print("\t\t{}:".format(kk))
                    for kkk, vvv in vv.items():
                        print("\t\t\t{}: {}".format(kkk, vvv))
                else:
                    print("\t\t{}: {}".format(kk, vv))


def test_producer():
    class DemoProducer(BaseProducer):
        pass

    p = DemoProducer()
    msg = {
        "data": "hello {}".format(datetime.datetime.now()),
    }
    p.publish(msg)


@pytest.mark.timeout(1)
def test_consumer():
    class DemoConsumer(BaseConsumer):
        def do_task(self, payload):
            print("queue task: {}".format(payload))
            # raise KeyboardInterrupt

    c = DemoConsumer()
    c.consume()  # 死循环, 不会退出, 需要外部结束掉测试, 正常验证结果.
