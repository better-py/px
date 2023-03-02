# -*- encoding:utf-8 -*-
import json
import logging
import pika
from django.conf import settings
from pika.adapters.blocking_connection import BlockingChannel

from ..utils import generate_sign_sha256, validate_sign_sha256, generate_nonce_8bit, generate_timestamp_13bit

logger = logging.getLogger(__name__)

#
# MQ 默认配置项:
#   - 移植使用时, 可扔掉 django.conf.settings, 替换如下全局参数
#
DEFAULT_MQ_URL = settings.RABBITMQ_URL
DEFAULT_MQ_CONTENT_TYPE = settings.RABBITMQ_CONTENT_TYPE
DEFAULT_MQ_CONFIG = settings.RABBITMQ_CONFIG_GROUP["default"]
DEFAULT_MQ_SIGN_SECRET_KEY = settings.RABBITMQ_SIGN_SECRET_KEY


class BaseMQService(object):
    MQ_URL = DEFAULT_MQ_URL
    MQ_CONTENT_TYPE = DEFAULT_MQ_CONTENT_TYPE
    #
    MQ_CONFIG_GROUPS = DEFAULT_MQ_CONFIG
    #
    MQ_SIGN_SECRET_KEY = DEFAULT_MQ_SIGN_SECRET_KEY

    def __init__(self, mq_url=None, mq_content_type=None, mq_conf_groups=None, secret_key=None):
        """

        :param mq_url:
        :param mq_content_type:
        :param mq_conf_groups: 多组队列配置, type=list
        """
        self.mq_url = mq_url or self.MQ_URL
        self.mq_content_type = mq_content_type or self.MQ_CONTENT_TYPE
        self.mq_conf_groups = mq_conf_groups or self.MQ_CONFIG_GROUPS
        if not isinstance(self.mq_conf_groups, list):
            self.mq_conf_groups = [self.mq_conf_groups]

        self.secret_key = secret_key or self.MQ_SIGN_SECRET_KEY

    def _connect(self):
        conn_params = pika.URLParameters(self.mq_url)
        conn = pika.BlockingConnection(conn_params)
        chan = conn.channel()
        return conn, chan

    def _setup(self, channel: BlockingChannel):
        """配置工作队列和死信队列

        :return:
        """
        for conf in self.mq_conf_groups:
            # 配置死信队列参数
            self._setup_queue(
                channel=channel,
                exchange=conf["arguments"]["x-dead-letter-exchange"],
                exchange_type=conf["exchange_type"],
                queue=conf["arguments"]["x-dead-letter-routing-key"],
                routing_key=conf["arguments"]["x-dead-letter-routing-key"],
            )

            # 配置工作队列参数
            self._setup_queue(
                channel=channel,
                exchange=conf["exchange"],
                exchange_type=conf["exchange_type"],
                queue=conf["queue"],
                routing_key=conf["routing_key"],
                arguments=conf["arguments"],  # 死信队列参数
            )

    @staticmethod
    def _setup_queue(channel: BlockingChannel, exchange, exchange_type, queue, routing_key, arguments=None):
        """ 声明 MQ 的交换器和队列, 已经队列绑定交换器

        :param channel:
        :param exchange:
        :param exchange_type:
        :param queue:
        :param routing_key: 路由键
        :param arguments: 设置死信队列参数
        :return:
        """
        channel.exchange_declare(
            exchange=exchange,
            exchange_type=exchange_type,
            durable=True,
            auto_delete=False,
        )
        channel.queue_declare(
            queue=queue,
            durable=True,
            auto_delete=False,
            arguments=arguments,
        )
        channel.queue_bind(
            queue=queue,
            exchange=exchange,
            routing_key=routing_key,
            arguments=arguments,
        )


# 队列: 生产者
class BaseProducer(BaseMQService):
    def publish(self, message: dict):
        # create conn:
        conn, chan = self._connect()
        self._setup(chan)
        #
        msg = self._format_message(message, channel=chan)
        self._on_publish(msg, chan)

    def _on_publish(self, message, channel: BlockingChannel):
        exchange = self.mq_conf_groups[0]["exchange"]
        routing_key = self.mq_conf_groups[0]["routing_key"]
        props = pika.BasicProperties(
            content_type=self.mq_content_type,
            delivery_mode=2,
        )  # 持久模式
        logger.info('^^publish msg  routing_key:{}|message body:{} ,exchange:{}, props:{}, channel, {}'.format(routing_key, message, exchange, props, channel))

        try:
            # 发布消息
            channel.basic_publish(
                exchange,
                routing_key,
                body=message,
                properties=props,
            )
        except Exception as e:
            raise e
        finally:
            channel.close()  # 关闭连接

    def _format_message(self, message: dict, channel: BlockingChannel):
        if not isinstance(message, dict):
            channel.close()
            raise TypeError("Invalid Message Type: [{}] must be dict object.".format(message))
        # add sign:
        message = self._sign_payload(message)
        return json.dumps(message, ensure_ascii=False)

    def _sign_payload(self, payload: dict):
        """计算签名, 并添加到 payload 中.

        - 自动添加 timestamp 和 nonce 字段, 防止重放攻击
        :param payload:
        :return:
        """
        # 补充字段: 防止重放攻击
        payload.update(
            nonce=generate_nonce_8bit(),
            timestamp=generate_timestamp_13bit(),
        )
        # 生成签名
        sign = generate_sign_sha256(
            payload=payload,
            secret_key=self.secret_key,
        )
        payload.update(sign=sign)
        return payload


# 队列: 消费者
class BaseConsumer(BaseMQService):
    def consume(self):
        # create conn:
        conn, chan = self._connect()
        self._setup(chan)
        #
        queue = self.mq_conf_groups[0]["queue"]
        # 处理:
        chan.basic_consume(self._on_message, queue=queue)
        try:
            chan.start_consuming()  # 开始消费
        except KeyboardInterrupt:
            chan.stop_consuming()  # 退出消费
        finally:
            chan.close()

    def _on_message(self, channel: BlockingChannel, method_frame, header_frame, body):
        """处理接收到的消息的回调函数

        :param channel:
        :param method_frame: 投递标记
        :param header_frame: AMQP信息头的对象
        :param body: 消息实体
        :return:
        """

        try:
            # bugfix: 提前 return 导致 异常时 basic_nack() 未被执行.
            logger.info("body:{}, {}".format(type(body), body))  # TODO: 需要清理, ENGINE_RPC_PARAMS

            payload = json.loads(body) if not isinstance(body, dict) else body

            if self._validate_payload(payload):
                self.do_task(payload)
            else:
                logger.error("invalid MQ Task: {}".format(payload))

            # 消息确认， 确认之后才会删除消息并给消费者发送新的消息
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        except Exception as e:
            logger.exception(e)
            logger.error("Dead-Letter-MQ # MSG_body: {}".format(body))
            # dead letter message
            channel.basic_nack(delivery_tag=method_frame.delivery_tag, requeue=False)

    def _validate_payload(self, payload: dict):
        """对数据作签名验证, 提取 sign 字段. 算签名作对比

        :param payload:
        :return:
        """
        payload_sign = payload.get("sign")
        if not payload_sign:
            return False
        payload.pop("sign")
        return validate_sign_sha256(payload, self.secret_key, input_sign=payload_sign)

    def do_task(self, payload: dict):
        """回调钩子: 用来做业务逻辑操作

        :param payload: 数据
        :return:
        """
        raise NotImplementedError
