import aioredis


class Redis:
    def __init__(self, loop, address):
        self.redis = loop.run_until_complete(
            aioredis.create_redis(address, loop=loop),
        )
