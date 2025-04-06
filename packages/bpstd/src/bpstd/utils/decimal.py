import logging
import math
from decimal import Decimal


logger = logging.getLogger(__name__)


def format_amount(amount: Decimal, scale=2):
    amount = Decimal(amount).normalize()
    amount = "{:.10f}".format(amount)
    amount = Decimal(amount).normalize()
    #
    amount = amount * (10**scale)
    amount = math.floor(amount) / (10**scale)
    # logger.info('amount:{}'.format(amount))
    # logger.info('format amount:{}'.format(Decimal(amount).normalize()))
    amount = str(float(amount))
    return amount if not amount.endswith(".0") else amount.rsplit(".0", 1)[0]
