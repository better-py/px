import logging

from geetest import GeetestLib
from django.conf import settings

logger = logging.getLogger(__name__)

captcha_id = settings.GEETEST_ID
private_key = settings.GEETEST_KEY

gt = GeetestLib(captcha_id, private_key)


def stage_one(user_id='btcc'):
    """初始化验证
    :param user_id: 选填 用于进阶分析
    :return: {"success": 1, "gt": "xx", "challenge": "xx"}, status
    gt 为captcha_id
    challenge 为唯一的行为编号 防止重放攻击

    status 为是否连接到geetest 服务器 如果为0 进行本地验证
    """

    # status 判断是否连接到geetest 服务器
    status, challenge = gt._register(user_id)
    response = dict(
        success=status,
        gt=gt.captcha_id,
        challenge=challenge
    )
    logger.info("id:{}-key:{} call stage_one".format(captcha_id, private_key))
    return status, response


def stage_two(challenge, validate, seccode, status, user_id='btcc'):
    if status:
        result = gt.success_validate(challenge, validate, seccode, user_id)
    else:
        result = gt.failback_validate(challenge, validate, seccode)
    logger.info("id:{}-key:{} call stage_two result:{}".format(captcha_id, private_key, result))
    return result
