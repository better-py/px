class SmsSender:
    """短信服务基类"""

    def send_code(self, mobile: str, country_code: str):
        raise NotImplementedError

    def _format_response(self):
        raise NotImplementedError

    @property
    def client(self):
        return self._client

    def _client(self, api_key, api_secret):
        raise NotImplementedError

    def __init__(self, api_key, api_secret):
        self._client(api_key, api_secret)
