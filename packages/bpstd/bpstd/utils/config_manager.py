import json
from json import JSONDecodeError

import consul


class ConfigCenter:
    """配置中心

    - 适合各种配置项: constants 常量参数

    """

    def __init__(self, host: str = "127.0.0.1", port: int = 8500):
        self.client = consul.Consul(host=host, port=port)

    def set(self, key: str, value):
        """格式化字典型数据

        :param key:
        :param value:
        :return:
        """
        if isinstance(value, dict):
            value = json.dumps(value)
        return self.client.kv.put(key, value)

    def gets(self, key: str):
        """返回值是字典型结构

        :param key:
        :return: type=dict
        """
        v = self.get(key=key)
        try:
            value = json.loads(v)
        except JSONDecodeError as e:
            value = v
        return value

    def get(self, key: str):
        """普通 str

        :param key:
        :return: type=str
        """
        _index, _value = self.client.kv.get(key=key)
        value = _value.get("Value").decode()
        return value

    def delete(self, key: str):
        return self.client.kv.delete(key=key)
