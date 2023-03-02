from decimal import Decimal
from pycoin.key.validate import is_address_valid as validate_btc_address

from .eth import validate_address as validate_eth_address
from maneki.apps.constants import CoinType


class CryptoCoinGroup(object):
    btc_group = (
        CoinType.BTC, CoinType.BCH,
    )

    eth_group = (
        CoinType.ETH, CoinType.ETC,
    )


ETHER_PER_WEI = Decimal(int(1e18))


def ether_to_wei(ether):
    if ether == 0:
        return Decimal(0)
    r = Decimal(ether) * ETHER_PER_WEI
    return r.normalize()


def validate_crypto_address(coin_type, address):
    if coin_type in CryptoCoinGroup.btc_group:
        if not validate_btc_address(address):
            raise ValueError

    if coin_type in CryptoCoinGroup.eth_group:
        validate_eth_address(address)
