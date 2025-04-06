from datetime import datetime

from tsidpy import TSIDGenerator


####################################################################################################

#
# twitter snowflake
#
_twitter_datacenter: int = 1
_twitter_worker: int = 1
_twitter_node: int = _twitter_datacenter << 5 | _twitter_worker
_twitter_epoch: datetime = datetime.fromisoformat("2010-11-04T01:42:54.657Z")

_twitter_generator: TSIDGenerator = TSIDGenerator(
    node=_twitter_node,
    node_bits=10,
    epoch=_twitter_epoch.timestamp() * 1000,
    random_fn=lambda n: 0,
)


####################################################################################################


#
# discord snowflake
#
_discord_worker: int = 1
_discord_process: int = 1
_discord_node: int = _discord_worker << 5 | _discord_process
_discord_epoch: datetime = datetime.fromisoformat("2015-01-01T00:00:00.000Z")

_discord_generator: TSIDGenerator = TSIDGenerator(
    node=_discord_node,
    node_bits=10,
    epoch=_discord_epoch.timestamp() * 1000,
)

####################################################################################################


def generate_19_digit(adopter: str = "twitter"):
    """雪花算法, 支持2个版本, 示例: 1908858723036696576

    Args:
        adopter (str, optional): 可选值为 `twitter` or `discord`

    Returns:
        id (int): 生成一个新的 ID 的`数字`表示, size=`19位`
    """
    if adopter.lower() == "discord":
        return _discord_generator.create().number
    return _twitter_generator.create().number


def generate_13_str(adopter: str = "twitter"):
    """雪花算法, 支持2个版本, 示例: 1MZD0WMGG4401

    Args:
        adopter (str, optional): 可选值为 `twitter` or `discord`

    Returns:
        id (int): 生成一个新的 ID 的`字符串`表示, size=`13位`
    """
    if adopter.lower() == "discord":
        return _discord_generator.create()
    return _twitter_generator.create()
